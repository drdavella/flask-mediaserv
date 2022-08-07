import socket
from os import environ
from time import sleep

from flask import Flask, request
from flask_cors import CORS
from flask_sock import Sock

from flask_migrate import Migrate

from .models import db
from .blueprints.api import api

if False:
    # For MySQL
    db_username = environ.get("DB_USERNAME", "development-only")
    db_password = environ.get("DB_PASSWORD", "development-only")
    db_uri = f"postgresql://{db_username}:{db_password}@postgres/momento-api"
else:
    db_uri = "sqlite:////var/lib/sqlite/data/mediaserv.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DATA_PATH"] = environ.get("MEDIASERV_DATA_PATH", "/data/music")

sock = Sock(app)

db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)

FRONTEND = r"https?://" + socket.gethostname() + ":3000"
CORS(app, resources={r"/api/*": {"origins": FRONTEND}})


app.register_blueprint(api)


@sock.route("/api/playback/status/")
def playback_status(ws):
    app.logger.debug("websocket: status")

    tick = 0
    while True:
        app.logger.debug("websocket tick: %d", tick)
        ws.send(tick)
        tick += 1
        sleep(1)
