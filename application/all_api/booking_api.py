from datetime import datetime
import os
from flask import jsonify, make_response, request
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from application import db
from application.models.booking import Booking
from application.models.rating import Rating
from application.models.product import Product

from application.models.category import Category

from ..validation import BadRequest, BusinessValidationError, NotFoundError, UnAuthorizedError
from ..models.user import User
from ..models.role import Role
from werkzeug.security import check_password_hash
from flask_restful import Resource, fields, marshal_with
from ..parser.bookingParser import booking_parser



class BookingAPI(Resource):

    @jwt_required()
    def post(self, user_id = None, category_id = None, product_id = None):
                
        errorMessages = []
        current_user_id = get_jwt_identity()
        if user_id is not None and user_id != current_user_id:
            errorMessages.append("You are not authorized to see the page")
            return UnAuthorizedError(error_messages=errorMessages)
        
        user = User.query.filter_by(id = user_id).first()
        if not user:
            errorMessages.append("User not found")
            return NotFoundError(error_messages=errorMessages)
        
        category = Category.query.filter_by(id = category_id).first()
        if not category:
            errorMessages.append("Category not found")
            return NotFoundError(error_messages=errorMessages)
        
        product = Product.query.filter_by(id = product_id).first()
        if not product:
            errorMessages.append("Product not found")
            return NotFoundError(error_messages=errorMessages)
        
        args = booking_parser.parse_args()
        numberOfProducts = args.get("number_of_products", None)
        totalPrice = args.get("total_price", None)

        
        new_booking = Booking(number_of_products=numberOfProducts , total_price=totalPrice, product_id=product_id, category_id=category_id, user_id=user_id)
        db.session.add(new_booking)
        db.session.commit()

        print(category.bookings)
        return make_response(jsonify({
                    "id" : new_booking.id,
                    "message" : "Booking done successfully"
                }), 201)

    @jwt_required()
    def get(self, user_id = None):

        errorMessages = []
        current_user_id = get_jwt_identity()
        if user_id is not None and user_id != current_user_id:
            errorMessages.append("You are not authorized to see the page")
            return UnAuthorizedError(error_messages=errorMessages)
        
        user = User.query.filter_by(id = user_id).first()
        if not user:
            errorMessages.append("User not found")
            return NotFoundError(error_messages=errorMessages)
        
        bookingsDto = []

        user_bookings = Booking.query.filter(Booking.user_id == user_id).all()

        for each_booking in user_bookings:
            product = Product.query.filter(Product.id == each_booking.product_id).first()
            category = Category.query.filter(Category.id == each_booking.category_id).first()
            rating = Rating.query.filter(Rating.booking_id == each_booking.id).first()
            if rating:
                rating_given = True
            else:
                rating_given = False
            booking = {
                "id": each_booking.id,
                "total_price": each_booking.total_price,
                "number_of_products": each_booking.number_of_products,
                "product_name": product.storedName,
                "product_id": product.id,
                "category_id":category.id,
                "category_name": category.storedName,  
                "is_rating_given": rating_given
            }
            bookingsDto.append(booking)

        return make_response(jsonify(bookingsDto), 200)