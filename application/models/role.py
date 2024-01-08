from application import db
from flask_login import UserMixin


class Role(db.Model, UserMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    storedName = db.Column(db.String, unique=True, nullable=False)
    storedUsers = db.relationship('User', backref='role', lazy=True, cascade="all,delete")