import os
from pathlib import Path

from flask import Blueprint, current_app, jsonify, request

from ..models import Album, Track

albums = Blueprint("albums", __name__, url_prefix="/albums")


@albums.route("", methods=["GET"])
def all_albums():
    current_app.logger.debug("all albums")
    return jsonify(Album.query.all())


@albums.route("/<album_id>", methods=["GET"])
def one_album(album_id):
    current_app.logger.debug("album by id: %s", album_id)
    return jsonify(Album.query.get(album_id))


@albums.route("/<album_id>/tracks", methods=["GET"])
def album_tracks(album_id):
    current_app.logger.debug("album tracks by id: %s", album_id)
    return jsonify(
        Track.query.filter(Track.album_id == album_id)
        .order_by(Track.disc_number)
        .order_by(Track.track_number)
        .all()
    )
