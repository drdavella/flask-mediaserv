import os
from os import environ, listdir
import socket
from time import sleep

from flask import Flask, request
from flask_cors import CORS
from flask_sock import Sock

from flask_migrate import Migrate
from sqlalchemy_utils import EmailType, PasswordType

from werkzeug.security import check_password_hash, generate_password_hash

from models.db import db
from blueprints.api import api

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
migrate = Migrate(app, db)

FRONTEND = r"https?://" + socket.gethostname() + ":3000"
CORS(app, resources={r"/api/*": {"origins": FRONTEND}})


app.register_blueprint(api)


@app.route("/api/search/<term>", methods=["GET"])
def search(term):
    app.logger.debug("search term: %s", term)
    return {"results": "", "search": term}


@app.route("/api/login/", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    app.logger.debug(f"login attempt: username={username}")

    user = User.query.filter_by(username=username).first()
    if user is None:
        app.logger.debug(f"login failed: unknown user")
        return {"success": False, "message": "Invalid login"}, 401

    if not user.check_password(password):
        app.logger.debug(f"login failed: invalid password")
        return {"success": False, "message": "Invalid login"}, 401

    app.logger.debug(f"login success")
    return {"success": True, "message": "Logged in"}


@app.route("/api/register/", methods=["POST"])
def register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    user = User.query.filter_by(username=username).first()
    if user is not None:
        app.logger.debug(f"attempted register, username exists: username={username}")
        return {"success": False, "message": "User already exists"}

    app.logger.debug(f"register: username={username}, email={email}")

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return {"success": True, "message": "User created"}


@app.route("/api/albums/", methods=["GET"])
def albums():
    app.logger.debug("albums")
    return {
        "albums": [
            {
                "name": "Whatever",
                "artist": "The Foos",
            },
            {
                "name": "Something Else",
                "artist": "The Bars",
            },
            {
                "name": "Sgt Peppers",
                "artist": "The Beatles",
            },
        ]
    }


@sock.route("/api/playback/status/")
def playback_status(ws):
    app.logger.debug("websocket: status")

    tick = 0
    while True:
        app.logger.debug("websocket tick: %d", tick)
        ws.send(tick)
        tick += 1
        sleep(1)
