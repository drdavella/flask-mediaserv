import socket
from os import environ
from time import sleep

from flask import Flask, request
from flask_cors import CORS
from flask_sock import Sock

from flask_migrate import Migrate

from .models import db
from .blueprints.api import api

DB_URI = "sqlite:////var/lib/sqlite/data/mediaserv.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
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
