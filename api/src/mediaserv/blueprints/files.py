import os
from collections import defaultdict
from pathlib import Path

import audio_metadata as am
from flask import Blueprint, current_app, request

from ..models.db import db
from ..models.album import Album
from ..models.scans import Scan

files = Blueprint("files", __name__, url_prefix="/files")

EXTENSIONS_TO_SKIP = ['.png', '.jpg']


@files.route("/", methods=["GET"])
def get_files():
    # TODO: use pathlib.Path here
    data_path = current_app.config.get("DATA_PATH")
    directory = request.args.get("directory", "")
    list_path = os.path.join(data_path, directory)
    safe_path = (
        os.path.sep + os.path.relpath(list_path, data_path)
        if directory
        else os.path.sep
    )
    current_app.logger.debug("File path requested: %s", list_path)

    if not os.path.exists(list_path):
        current_app.logger.debug("Requested file directory not found: %s", list_path)
        return {"message": "No such file/directory"}, 404  # TODO: is this right?

    # Prevent path traversal outside the data directory tree
    if os.path.commonpath([data_path, list_path]) != os.path.abspath(data_path):
        return {"message": directory}, 403

    if os.path.isfile(list_path):
        basename = os.path.basename(list_path)
        return {
            "files": [
                {
                    "name": basename.replace("-", " ").replace("_", " "),
                    "full_path": os.path.sep + os.path.relpath(list_path, data_path),
                    "is_directory": False,
                },
            ],
            "directory": os.path.dirname(safe_path),
        }

    files = os.listdir(list_path)

    result = {"files": [], "directory": safe_path}
    for f in files:
        full_path = os.path.join(list_path, f)
        result["files"].append(
            {
                "name": f.replace("-", " ").replace("_", " "),
                "full_path": os.path.join(safe_path, f),
                "is_directory": os.path.isdir(full_path),
            }
        )

    return result


@files.route("/scan", methods=["POST"])
def scan_directory():
    data_path = Path(current_app.config.get("DATA_PATH"))
    directory = Path(request.args.get("directory", ""))
    list_path = data_path / directory
    current_app.logger.debug("list path: %s", list_path)

    job_id = Scan.record_scan(directory)

    # TODO: refactor into separate library module
    albums = defaultdict(list)
    for filename in list_path.rglob("*"):
        if os.path.isdir(filename):
            continue

        # TODO: record image filenames with associated directories/albums
        if filename.suffix in EXTENSIONS_TO_SKIP:
            current_app.logger.debug("Skipping file because of extension: %s", filename)
            continue

        try:
            meta = am.load(filename)
        except am.exceptions.UnsupportedFormat as e:
            current_app.logger.debug("%s: (filename=%s)", e, filename)
            continue

        if album_name := meta.tags.album[0]:
            albums[album_name].append((filename, meta))

    for album_name, tracks in albums.items():
        for filename, meta in tracks:
            pass

    return {'job_id': job_id}

@files.route("/scan/status", methods=["GET"])
def scan_status():
    job_id = request.args.get("job_id", "")
    return {}
