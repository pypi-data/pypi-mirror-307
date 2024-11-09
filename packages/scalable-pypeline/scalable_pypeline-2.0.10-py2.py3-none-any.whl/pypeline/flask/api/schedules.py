""" API Endpoints for Scheduled Tasks
"""
import os
import logging
from flask import jsonify, request
from flask.views import MethodView
from marshmallow import Schema, fields
from flask_smorest import Blueprint
from flask import abort
from marshmallow.exceptions import ValidationError
from pypeline.constants import API_DOC_RESPONSES, API_DOC_PARAMS, API_PATH_V1
from pypeline.utils.config_utils import retrieve_latest_schedule_config
from pypeline.schedule_config_schema import BaseScheduleSchema
from pypeline.flask.decorators import require_accesskey

logger = logging.getLogger(__name__)

bp = Blueprint("schedules", __name__, url_prefix=API_PATH_V1 + "/schedules")


@bp.route("/")
class Schedules(MethodView):
    """Operations related to schedules"""

    @require_accesskey
    @bp.doc(
        responses=API_DOC_RESPONSES,
        parameters=[API_DOC_PARAMS["accesskey"]],
        tags=["Schedules"],
    )
    def get(self):
        """Retrieve list of available schedule entries."""
        access_key = request.headers.get("accesskey")
        try:
            schedule_config = retrieve_latest_schedule_config()
        except ValidationError:
            abort(400, message="Invalid schedule found ...")

        if schedule_config is None:
            abort(404)

        return jsonify(schedule_config)
