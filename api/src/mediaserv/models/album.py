from dataclasses import dataclass

from sqlalchemy_imageattach.entity import Image, image_attachment

from .db import db


class AlbumImage(db.Model, Image):
    id = db.Column(db.Integer, db.ForeignKey("album.id"), primary_key=True)
    album = db.relationship("Album")


@dataclass
class Album(db.Model):
    id: int
    name: str
    num_discs: int
    year: str
    image_uri: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    num_discs = db.Column(db.Integer, nullable=False, default=1)

    year = db.Column(db.String)

    # Do we want to collect all composers/artists/genres here as well?

    tracks = db.relationship("Track", back_populates="album")

    album_image = image_attachment("AlbumImage")

    added_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    @property
    def image_uri(self):
        try:
            return self.album_image.locate()
        except IOError:
            return ""
