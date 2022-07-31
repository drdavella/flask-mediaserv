from .db import db


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    tracks = db.relationship("Track", back_populates="album")
