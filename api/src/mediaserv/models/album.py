from .db import db


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    num_discs = db.Column(db.Integer, nullable=False, default=1)

    # album_artist
    # date?

    # Do we want to collect all composers/artists/genres here as well?

    tracks = db.relationship("Track", back_populates="album")

    added_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
