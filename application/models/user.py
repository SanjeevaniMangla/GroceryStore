from datetime import datetime
from application import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    stored_email = db.Column(db.String(64), unique=True, nullable=False)
    stored_username = db.Column(db.String(64), unique=True, nullable=False)
    stored_password = db.Column(db.String(64), unique=True, nullable=False)
    last_visited = db.Column(db.DateTime, default=datetime.now)
    report_format = db.Column(db.String(64), default="HTML")
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    categories = db.relationship('Category', backref='creator', lazy='dynamic', cascade="all,delete")
    products = db.relationship('Product', backref='creator', lazy='dynamic', cascade="all,delete")
    booked = db.relationship('Booking', backref='user', lazy='dynamic', cascade="all,delete")
    ratings = db.relationship('Rating', backref='user', lazy='dynamic', cascade="all,delete")