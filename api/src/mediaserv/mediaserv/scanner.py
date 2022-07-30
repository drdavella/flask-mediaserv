import os
from collections import defaultdict
from pathlib import Path
from threading import Thread

import audio_metadata as am
from flask import current_app, copy_current_request_context

from ..models import db
from ..models.scan import Scan


IMAGE_EXTENSIONS = [".png", ".jpg"]


def run_scan(directory: Path, job_id: str, current_app):
    current_app.logger.debug("beginning path: %s (job_id=%s)", directory, job_id)

    albums = defaultdict(list)
    for filename in directory.rglob("*"):
        if os.path.isdir(filename):
            continue

        # TODO: record image filenames with associated directories/albums
        if filename.suffix in IMAGE_EXTENSIONS:
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

    Scan.mark_finished(job_id)
    current_app.logger.info("Scan complete: %s (job_id=%s)", directory, job_id)


def start_scan_directory(directory: Path):
    data_path = Path(current_app.config.get("DATA_PATH"))
    list_path = data_path / directory

    @copy_current_request_context
    def scan_directory(directory: Path, job_id: str):
        run_scan(directory, job_id, current_app)

    # TODO: refactor into separate library module
    job_id = Scan.record_scan(directory)
    thread = Thread(target=scan_directory, args=(list_path, job_id))
    thread.start()

    return job_id
