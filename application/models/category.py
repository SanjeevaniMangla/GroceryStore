from datetime import datetime
from application import db


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    storedName = db.Column(db.String, nullable=False)
    storedImage = db.Column(db.String, default="", unique=True, nullable=False)
    created_date_time = db.Column(db.DateTime, default=datetime.now)
    updated_date_time = db.Column(db.DateTime, default=datetime.now)
    createdby_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    products_under_category = db.relationship('Product', secondary='product_category_association', back_populates='categories')
    bookings = db.relationship('Booking', backref='category', cascade="all,delete")
    ratings = db.relationship('Rating', backref='category', cascade="all,delete")