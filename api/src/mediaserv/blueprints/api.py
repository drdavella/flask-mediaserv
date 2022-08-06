from flask import Blueprint

from .files import files
from .albums import albums


api = Blueprint("api", __name__, url_prefix="/api")
api.register_blueprint(files)
api.register_blueprint(albums)
