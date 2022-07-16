from flask import Blueprint

from .files import files


api = Blueprint("api", __name__, url_prefix="/api")
api.register_blueprint(files)
