import os
from collections import defaultdict
from pathlib import Path
from threading import Thread

import audio_metadata as am
from flask import current_app, copy_current_request_context
from sqlalchemy_imageattach.context import store_context

from ..models import Album, Artist, Track, Scan, db


IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg"]
IGNORE_EXTENSIONS = [".pdf"]


def run_scan(directory: Path, job_id: str, current_app):
    current_app.logger.debug("beginning path: %s (job_id=%s)", directory, job_id)

    albums = defaultdict(list)
    image_files = defaultdict(list)
    image_blobs = {}
    album_images = {}

    # TODO: this loop can be parallelized
    for filename in directory.rglob("*"):
        if os.path.isdir(filename):
            continue

        dirname = os.path.dirname(filename)
        if filename.suffix in IMAGE_EXTENSIONS:
            current_app.logger.debug("Detected image file: %s", filename)
            image_files[dirname].append(filename)
            continue

        if filename.suffix in IGNORE_EXTENSIONS:
            current_app.logger.debug("Ignoring file with unsupported extension: %s", filename)
            continue

        try:
            meta = am.load(filename)
        except am.exceptions.UnsupportedFormat as e:
            current_app.logger.debug("%s: (filename=%s)", e, filename)
            continue

        if album_name := meta.tags.album[0]:
            albums[album_name].append((filename, meta))
            if not album_name in image_blobs and meta.pictures:
                image_blobs[album_name] = meta.pictures[0]
            if not album_name in album_images and dirname in image_files:
                album_images[album_name] = image_files[dirname]

    for album_name, tracks in albums.items():
        current_app.logger.debug('album: %s', album_name)
        album = Album(name=album_name)
        db.session.add(album)
        album_discs = set()
        for filename, meta in tracks:
            disc_number = meta.tags.get('discnumber', [1])[0]
            album_discs.add(disc_number)
            if (not album.year) and (year := meta.tags.get('date', [])):
                album.year = year[0]

            track_meta = dict(
                title=meta.tags.title[0],
                disc_number=disc_number,
                track_number=meta.tags.tracknumber[0],
                uri=filename.as_uri(),
                # TODO: handle other encodings
                encoding='flac',
            )
            track = Track(album=album, **track_meta)
            db.session.add(track)
        album.num_discs = len(album_discs)

        with store_context(current_app.image_store):
            # TODO: generate thumbnails
            if album_name in image_blobs:
                album.album_image.from_blob(image_blobs[album_name].data)
            elif album_name in album_images and album_images[album_name]:
                with open(album_images[album_name][0], 'rb') as fh:
                    album.album_image.from_file(fh)
            else:
                current_app.logger.warn("No album art found for: \"%s\"", album_name)

            # Needs to occur within storage context
            db.session.commit()

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
