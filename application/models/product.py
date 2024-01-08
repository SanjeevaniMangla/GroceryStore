from datetime import datetime
from application import db


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    storedName = db.Column(db.String, nullable=False)
    storedPrice = db.Column(db.Integer, nullable=False)
    created_date_time = db.Column(db.DateTime, default=datetime.now)
    updated_date_time = db.Column(db.DateTime, default=datetime.now)
    categories = db.relationship('Category', secondary='product_category_association', back_populates='products_under_category')
    createdby_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bookings = db.relationship('Booking', backref='show', cascade="all,delete")
    ratings = db.relationship('Rating', backref='show', cascade="all,delete")