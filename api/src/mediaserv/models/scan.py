from shortuuid import uuid

from .db import db


class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String, nullable=False)
    directory = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    is_finished = db.Column(db.Boolean, default=False)

    # TODO: this logic probably doesn't really belong with the model itself
    @staticmethod
    def record_scan(directory):
        job_id = uuid()
        scan_job = Scan(job_id=job_id, directory=str(directory))
        db.session.add(scan_job)
        db.session.commit()
        return job_id

    @staticmethod
    def mark_finished(job_id):
        db.session.query(Scan).filter(Scan.job_id == job_id).update(
            {"is_finished": True}
        )
        db.session.commit()
