from dataclasses import dataclass

from .db import db


@dataclass
class Track(db.Model):
    id: int
    title: str
    disc_number: int
    track_number: int
    encoding: str

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    uri = db.Column(db.String, nullable=False)
    disc_number = db.Column(db.Integer, nullable=False)
    track_number = db.Column(db.Integer, nullable=False)

    album_id = db.Column(db.Integer, db.ForeignKey("album.id"))
    album = db.relationship("Album", back_populates="tracks")

    # artists
    # composers
    # genre(s)

    added_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    encoding = db.Column(db.String, nullable=False)
    # sample_rate
    # bitrate (mp3)
    # bit_depth (flac)
    # duration
