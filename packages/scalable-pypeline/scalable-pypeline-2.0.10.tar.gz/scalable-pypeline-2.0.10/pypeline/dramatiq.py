import importlib
import os.path
import sys
import typing
import pika
import logging

import click
from urllib.parse import urlparse

from pypeline.extensions import pypeline_config
from warnings import warn
from functools import wraps
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from typing import Awaitable, Callable, Optional, Union, TYPE_CHECKING, TypeVar
from dramatiq import Broker, Middleware, actor as register_actor, set_broker, get_broker
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.cli import (
    CPUS,
    HAS_WATCHDOG,
    main as dramatiq_worker,
    make_argument_parser as dramatiq_argument_parser,
    import_object,
)
from dramatiq.middleware import default_middleware, CurrentMessage
from dramatiq.results import Results
from dramatiq.results.backends.redis import RedisBackend
from flask import current_app, Flask
from flask.cli import with_appcontext

from pypeline.constants import (
    REDIS_URL,
    RABBIT_URL,
    DEFAULT_BROKER_CALLABLE,
    MS_IN_SECONDS,
    DEFAULT_TASK_TTL,
    DEFAULT_RESULT_TTL,
    DEFAULT_TASK_MAX_RETRY,
    DEFAULT_TASK_MIN_BACKOFF,
    DEFAULT_TASK_MAX_BACKOFF,
    DEFAULT_BROKER_CONNECTION_HEARTBEAT,
    DEFAULT_BROKER_BLOCKED_CONNECTION_TIMEOUT,
    DEFAULT_BROKER_CONNECTION_ATTEMPTS,
)
from pypeline.middleware import ParallelPipeline
from pypeline.utils.config_utils import (
    retrieve_latest_schedule_config,
    get_service_config_for_worker,
)

if TYPE_CHECKING:
    from typing_extensions import ParamSpec

    P = ParamSpec("P")
else:
    P = TypeVar("P")
R = TypeVar("R")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def configure_default_broker(broker: Broker = None):
    redis_backend = RedisBackend(url=REDIS_URL)
    parsed_url = urlparse(RABBIT_URL)
    credentials = pika.PlainCredentials(parsed_url.username, parsed_url.password)
    rabbit_broker = (
        broker
        if broker is not None
        else RabbitmqBroker(
            host=parsed_url.hostname,
            port=parsed_url.port,
            credentials=credentials,
            heartbeat=DEFAULT_BROKER_CONNECTION_HEARTBEAT,
            connection_attempts=DEFAULT_BROKER_CONNECTION_ATTEMPTS,
            blocked_connection_timeout=DEFAULT_BROKER_BLOCKED_CONNECTION_TIMEOUT,
        )
    )
    rabbit_broker.add_middleware(Results(backend=redis_backend))
    rabbit_broker.add_middleware(ParallelPipeline(redis_url=REDIS_URL))
    rabbit_broker.add_middleware(CurrentMessage())
    register_actors_for_workers(rabbit_broker)
    set_broker(rabbit_broker)


def guess_code_directory(broker):
    actor = next(iter(broker.actors.values()))
    modname, *_ = actor.fn.__module__.partition(".")
    mod = sys.modules[modname]
    return os.path.dirname(mod.__file__)


def get_module(resource_dot_path: str):
    """Retrieve the module based on a 'resource dot path'.
    e.g. package.subdir.feature_file.MyCallable
    """
    module_path = ".".join(resource_dot_path.split(".")[:-1])
    module = importlib.import_module(module_path)
    return module


def get_callable_name(resource_dot_path: str) -> str:
    """Retrieve the callable based on config string.
    e.g. package.subdir.feature_file.MyCallable
    """
    callable_name = resource_dot_path.split(".")[-1]
    return callable_name


def get_callable(resource_dot_path: str) -> Callable:
    """Retrieve the actual handler class based on config string.
    e.g. package.subdir.feature_file.MyCallable
    """
    module = get_module(resource_dot_path)
    callable_name = get_callable_name(resource_dot_path)
    return getattr(module, callable_name)


def register_lazy_actor(
    broker: Broker,
    fn: Optional[Callable[P, Union[Awaitable[R], R]]] = None,
    pipeline_meta: typing.Dict = {},
    **kwargs,
) -> typing.Type["LazyActor"]:
    kwargs["queue_name"] = pipeline_meta.get("queue", "default")
    kwargs["max_retries"] = pipeline_meta.get("maxRetry", DEFAULT_TASK_MAX_RETRY)
    # Convert from seconds to milliseconds
    kwargs["min_backoff"] = (
        pipeline_meta.get("retryBackoff", DEFAULT_TASK_MIN_BACKOFF) * MS_IN_SECONDS
    )
    kwargs["max_backoff"] = (
        pipeline_meta.get("retryBackoffMax", DEFAULT_TASK_MAX_BACKOFF) * MS_IN_SECONDS
    )
    kwargs["time_limit"] = pipeline_meta.get("maxTtl", DEFAULT_TASK_TTL) * MS_IN_SECONDS
    # Always store results for registered pipeline actors
    kwargs["store_results"] = pipeline_meta.get("store_results", False)
    if kwargs["store_results"]:
        kwargs["result_ttl"] = (
            pipeline_meta.get("result_ttl", DEFAULT_RESULT_TTL) * MS_IN_SECONDS
        )
    lazy_actor: LazyActor = LazyActor(fn, kwargs)
    lazy_actor.register(broker)
    return lazy_actor


def register_actors_for_workers(broker: Broker):
    service = get_service_config_for_worker(pypeline_config)
    scheduled_jobs_config = retrieve_latest_schedule_config()

    if not service:
        return
    for task in service.get("registeredTasks", []):
        pipeline_meta = None
        for pipeline_key, pipeline in pypeline_config["pipelines"].items():
            pipeline_config = pipeline["config"]
            pipeline_tasks = [
                t["handler"] for t in pipeline_config["taskDefinitions"].values()
            ]
            if task["handler"] in pipeline_tasks:
                pipeline_meta = pipeline_config["metadata"]
                break

        if pipeline_meta is None:
            for job in scheduled_jobs_config:
                config = job["config"]
                if config["task"] == task["handler"]:
                    pipeline_meta = {"queue": config.get("queue", "default")}

        if pipeline_meta is None:
            raise ValueError(
                f"Registered task {task['handler']} is not defined in a pipeline or scheduled task"
            )

        try:
            worker_path = task["handler"]  # Required, no default
            tmp_handler = get_callable(worker_path)
            if pipeline_meta and pipeline_meta.get("maxRetry", 0) >= 0:
                pipeline_meta["store_results"] = True
                _ = register_lazy_actor(broker, tmp_handler, pipeline_meta)
        except Exception as e:
            logger.exception(f"Unable to add a task to dramatiq: {e}")


class Dramatiq:
    """Flask extension bridging Dramatiq broker and Flask app.

    Dramatiq API is eager. Broker initialisation precede actor declaration.
    This breaks application factory pattern and other way to initialize
    configuration after import.

    This class enables lazy initialization of Dramatiq. Actual Dramatiq broker
    is instanciated only once Flask app is created.

    .. automethod:: actor
    .. automethod:: init_app
    """

    def __init__(
        self,
        app: Flask = None,
        name: str = "dramatiq",
        config_prefix: str = None,
        middleware: typing.List[Middleware] = None,
    ):
        """
        :app: Flask application if created. See :meth:`init_app`.

        :param broker_configuration_callable_module: In order to work in fork and spawn mode
            we need to configure our broker using a callable function.  Default is specified as
            "pypeline.flask_dramatiq:configure_default_broker".  This allows the user to
            override if necessary.

        :param name: Unique identifier for multi-broker app.

        :param config_prefix: Flask configuration option prefix for this
            broker. By default, it is derived from ``name`` parameter,
            capitalized.

        :param middleware: List of Dramatiq middleware instances to override
             Dramatiq defaults.

        Flask-Dramatiq always prepend a custom middleware to the middleware
        stack that setup Flask context. This way, every middleware can use
        Flask app context.

        """
        self.actors = []
        self.app = None
        self.config_prefix = config_prefix or name.upper() + "_BROKER"
        self.name = name
        self.broker = None
        if middleware is None:
            middleware = [m() for m in default_middleware]
        self.middleware = middleware
        if app:
            self.init_app(app)

    def __repr__(self) -> str:
        return "<%s %s>" % (self.__class__.__name__, self.name)

    def init_app(self, app: Flask):
        """Initialize extension for one Flask application

        This method triggers Dramatiq broker instantiation and effective actor
        registration.

        """
        if self.app is not None:
            warn(
                "%s is used by more than one flask application. "
                "Actor's context may be set incorrectly." % (self,),
                stacklevel=2,
            )
        self.app = app
        app.extensions["dramatiq-" + self.name] = self

        module_name, broker_or_callable = import_object(DEFAULT_BROKER_CALLABLE)

        # Callable function is expected to setBroker()
        if callable(broker_or_callable):
            logger.info(f"Configuring broker via {DEFAULT_BROKER_CALLABLE}")
            broker_or_callable()
        else:
            raise TypeError("DEFAULT_BROKER_CALLABLE must point to a callable function")
        self.broker = get_broker()
        for actor in self.actors:
            actor.register(broker=self.broker)

    def actor(self, fn=None, **kw):
        """Register a callable as Dramatiq actor.

        This decorator lazily register a callable as a Dramatiq actor. The
        actor can't be called before :meth:`init_app` is called.

        :param kw: Keywords argument passed to :func:`dramatiq.actor`.

        """
        # Substitute dramatiq.actor decorator to return a lazy wrapper. This
        # allows to register actors in extension before the broker is
        # effectively configured by init_app.

        def decorator(fn):
            lazy_actor = LazyActor(self, fn, kw)
            self.actors.append(lazy_actor)
            if self.app:
                lazy_actor.register(self.broker)
            return lazy_actor

        if fn:
            return decorator(fn)
        return decorator


def format_actor(actor):
    return "%s@%s" % (actor.actor_name, actor.queue_name)


def ensure_return_value(default_value=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Call the original function
            result = func(*args, **kwargs)
            # Check if the function has returned a value
            if result is None:
                # Return the default value if the function returned None
                return default_value
            return result

        return wrapper

    return decorator


class LazyActor(object):
    # Intermediate object that register actor on broker an call.

    def __init__(self, fn, kw):
        self.fn = fn
        self.kw = kw
        self.actor = None

    def __call__(self, *a, **kw):
        return self.fn(*a, **kw)

    def __repr__(self):
        return "<%s %s.%s>" % (
            self.__class__.__name__,
            self.fn.__module__,
            self.fn.__name__,
        )

    def __getattr__(self, name):
        if not self.actor:
            raise AttributeError(name)
        return getattr(self.actor, name)

    def register(self, broker):
        self.actor = register_actor(
            actor_name=f"{self.fn.__module__}.{self.fn.__name__}",
            broker=broker,
            **self.kw,
        )(ensure_return_value(default_value=True)(self.fn))

    # Next is regular actor API.
    def send(self, *a, **kw):
        return self.actor.send(*a, **kw)

    def message(self, *a, **kw):
        return self.actor.message(*a, **kw)

    def send_with_options(self, *a, **kw):
        return self.actor.send_with_options(*a, **kw)


def list_managed_actors(broker, queues):
    queues = set(queues)
    all_actors = broker.actors.values()
    if not queues:
        return all_actors
    else:
        return [a for a in all_actors if a.queue_name in queues]


@click.command("cron-scheduler")
def cron_scheduler():  # pragma: no cover
    # Configure our broker that we will schedule registered tasks for
    scheduler = BlockingScheduler()
    module_name, broker_or_callable = import_object(DEFAULT_BROKER_CALLABLE)

    # Callable function is expected to setBroker()
    if callable(broker_or_callable):
        logger.info(f"Configuring broker via {DEFAULT_BROKER_CALLABLE}")
        broker_or_callable()
    else:
        raise TypeError("DEFAULT_BROKER_CALLABLE must point to a callable function")

    broker = get_broker()
    jobs = retrieve_latest_schedule_config()

    for job in jobs:
        if job["enabled"]:
            config = job["config"]
            worker_path = config["task"]
            tmp_handler = get_callable(worker_path)
            pipeline_meta = {"queue": config.get("queue", "default")}
            actor = register_lazy_actor(broker, tmp_handler, pipeline_meta)
            schedule = config["schedule"]
            scheduler.add_job(
                actor.send,
                CronTrigger.from_crontab(
                    f"{schedule['minute']} {schedule['hour']} {schedule['dayOfMonth']} {schedule['monthOfYear']} {schedule['dayOfWeek']}"
                ),
            )

    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()


@click.command("pypeline-worker")
@click.argument("broker_name", default="dramatiq")
@click.option(
    "-v", "--verbose", default=0, count=True, help="turn on verbose log output"
)
@click.option(
    "-p",
    "--processes",
    default=CPUS,
    metavar="PROCESSES",
    show_default=True,
    help="the number of worker processes to run",
)
@click.option(
    "-t",
    "--threads",
    default=8,
    metavar="THREADS",
    show_default=True,
    help="the number of worker treads per processes",
)
@click.option(
    "-Q",
    "--queues",
    type=str,
    default=None,
    metavar="QUEUES",
    show_default=True,
    help="listen to a subset of queues, comma separated",
)
@click.option(
    "--use-spawn",
    type=bool,
    default=False,
    metavar="USE_SPAWN",
    show_default=True,
    help="start processes by spawning (default: fork on unix, spawn on windows)",
)
@with_appcontext
def pypeline_worker(
    verbose, processes, threads, queues, broker_name, use_spawn
):  # pragma: no cover
    """Run dramatiq workers.

    Setup Dramatiq with broker and task modules from Flask app.

    \b
    examples:
      # Run dramatiq with 1 thread per process.
      $ flask worker --threads 1

    \b
      # Listen only to the "foo" and "bar" queues.
      $ flask worker -Q foo,bar

    \b
      # Consuming from a specific broker
      $ flask worker mybroker
    """
    # Plugin for flask.commands entrypoint.
    #
    # Wraps dramatiq worker CLI in a Flask command. This is private API of
    # dramatiq.

    parser = dramatiq_argument_parser()

    # Set worker broker globally.
    needle = "dramatiq-" + broker_name
    broker = current_app.extensions[needle].broker
    set_broker(broker)

    command = [
        "--processes",
        str(processes),
        "--threads",
        str(threads),
        # Fall back to flask_dramatiq global broker
        DEFAULT_BROKER_CALLABLE,
    ]

    if use_spawn:
        command += ["--use-spawn"]

    if current_app.config["DEBUG"]:
        verbose = max(1, verbose)
        if HAS_WATCHDOG:
            command += ["--watch", guess_code_directory(broker)]

    queues = queues.split(",") if queues else []
    if queues:
        command += ["--queues"] + queues
    command += verbose * ["-v"]
    args = parser.parse_args(command)
    logger.info("Able to execute the following actors:")
    for actor in list_managed_actors(broker, queues):
        logger.info("    %s.", format_actor(actor))

    dramatiq_worker(args)
