# app/views/errors.py
from flask import Blueprint
from werkzeug.exceptions import HTTPException
from .responses import error

errors_bp = Blueprint("errors", __name__)

@errors_bp.app_errorhandler(HTTPException)
def handle_http_exception(e: HTTPException):
    return error(message=e.description or e.name,
                 code=e.name.upper().replace(" ", "_"),
                 status=e.code or 500)

@errors_bp.app_errorhandler(Exception)
def handle_exception(e: Exception):
    # en dev puedes incluir str(e) en details
    return error(message="Internal Server Error", code="INTERNAL_ERROR", status=500)
