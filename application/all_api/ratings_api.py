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
from ..parser.ratingParser import rating_parser



class RatingsAPI(Resource):

    @jwt_required()
    def post(self, user_id = None, category_id = None, product_id = None, booking_id = None):
                
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
             

        args = rating_parser.parse_args()
        input_rating = args.get("rating", None)
        print(input_rating)
        new_rating = Rating(rating = input_rating, product_id=product_id, category_id=category_id, user_id=user_id, booking_id=booking_id)
        db.session.add(new_rating)
        db.session.commit()

        return make_response(jsonify({
                    "message" : "Booking done successfully"
                }), 201)