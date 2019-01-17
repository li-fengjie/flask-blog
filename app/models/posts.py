from app.exts import db
from datetime import datetime


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    rid = db.Column(db.Integer, index=True, default=0)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
