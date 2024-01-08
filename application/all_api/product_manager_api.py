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
from application.decorator1 import manager_required

from ..validation import BadRequest, BusinessValidationError, NotFoundError, UnAuthorizedError
from ..models.user import User
from ..models.role import Role
from werkzeug.security import check_password_hash
from flask_restful import Resource, fields, marshal_with
from ..parser.ratingParser import rating_parser
from ..parser.productParser import product_parser



class ProductManagerAPI(Resource):

    @jwt_required()
    @manager_required
    def post(self, user_id = None, category_id = None):

        errorMessages = []
        
        user = User.query.filter_by(id = user_id).first()
        if not user:
            errorMessages.append("User not found")
            return NotFoundError(error_messages=errorMessages)
        
        category = Category.query.filter_by(id = category_id).first()
        if not category:
            errorMessages.append("Category not found")
            return NotFoundError(error_messages=errorMessages)
        
        args = product_parser.parse_args()
        input_name = args.get("input_name", None)
        input_price = args.get("input_price", None)
        

        if not input_name:
            errorMessages.append("Name cannot be empty")
        if not input_price:
            errorMessages.append("Price cannot be empty")
        
        
        if len(errorMessages) != 0:
            raise BusinessValidationError(error_messages=errorMessages)
        

        existing_product = Product.query.filter_by(
                storedName=input_name,
                storedPrice=input_price
            ).first()

        if existing_product:
            # Check if the existing product is associated with the same category
            if existing_product in category.products_under_category:
                errorMessages.append("Product with the same details already exists in this Category")
                return BadRequest(error_messages=errorMessages)
            else:
                # If the existing show is not associated with this theatre, associate it
                category.products_under_category.append(existing_product)
                db.session.commit()
                return make_response(jsonify({
                    "message": "Product already exists and is now associated with this Category"
                }), 201)
        else:
            # If the product does not exist, create a new product and associate it with the category
            new_product = Product(
                storedName=input_name,
                storedPrice=input_price,
                createdby_id=user.id
            )
            category.products_under_category.append(new_product)
            db.session.add(new_product)
            db.session.commit()
            return make_response(jsonify({
                    "id": new_product.id,
                    "message" : "Product created successfully"
                }), 201)
        
    
    @jwt_required()
    def get(self, user_id = None, category_id = None, product_id = None):

        errorMessages = []
        product_list = []
        current_user_id = get_jwt_identity()
        if user_id is None:
            errorMessages.append("User is required to retrieve product")
            return BusinessValidationError(error_messages=errorMessages)

        if user_id is not None and user_id != current_user_id:
            errorMessages.append("You are not authorized to see the page")
            return UnAuthorizedError(error_messages=errorMessages)
        
        user = User.query.filter_by(id = user_id).first()
        if not user:
            errorMessages.append("User not found")
            return NotFoundError(error_messages=errorMessages)
        
        if category_id is None:
            errorMessages.append("Category is required to retrieve product")
            return BusinessValidationError(error_messages=errorMessages)
        
        category = Category.query.filter_by(id = category_id).first()
        if not category:
            errorMessages.append("Category not found")
            return NotFoundError(error_messages=errorMessages)
        

        if product_id is None:
            products = category.products_under_category.all()
            for product in products:
                product_data = {
                "id": product.id,
                "name": product.storedName,
                "rating": product.storedRating,
                "price": product.storedPrice,
                "created_by": user.id
                # Add more fields as needed
                }
                product_list.append(product_data)

            if products is None:
                errorMessages.append("There is no products")
                raise NotFoundError(error_messages=errorMessages)
            else:
                return make_response(jsonify({"products": product_list}), 200)
        else:
            product = Product.query.filter_by(id = product_id).first()
            if not product:
                errorMessages.append("There is no Product")
                raise BadRequest(error_messages=errorMessages)
            else:
                product_data = {
                "id": product.id,
                "name": product.storedName,
                "rating": product.storedRating,
                "price": product.storedPrice,
                "created_by": user.id
                # Add more fields as needed
                }
                return make_response(jsonify(product_data), 200)
            
    @jwt_required()
    @manager_required
    def put(self, user_id = None, category_id = None, product_id = None):

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
            raise NotFoundError(error_messages=errorMessages)
        
        args = product_parser.parse_args()
        input_name = args.get("input_name", None)
        input_price = args.get("input_price", None)

        if not input_name:
            errorMessages.append("Name cannot be empty")
        if not input_price:
            errorMessages.append("Price cannot be empty")
        
        
        if len(errorMessages) != 0:
            raise BusinessValidationError(error_messages=errorMessages)
    

        existing_product = Product.query.filter_by(
                storedName=input_name,
                storedPrice=input_price,
            ).first()

        if existing_product and existing_product != product:
            raise BusinessValidationError(error_messages=["Product with the same details already exists"])

        product.storedName = input_name
        product.storedPrice = input_price
        db.session.commit()
        return make_response(jsonify({
            "message": "Product updated successfully"
        }), 200)
        

    @jwt_required()
    @manager_required
    def delete(self, user_id = None, category_id = None, product_id = None):

        errorMessages = []
        current_user_id = get_jwt_identity()
        if user_id is not None and user_id != current_user_id:
            errorMessages.append("You are not authorized to the URL")
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
            raise NotFoundError(error_messages=errorMessages)
        
        db.session.delete(product)
        db.session.commit()
        return make_response(jsonify({"message" : "Product successfully deleted"}), 200)


        

        