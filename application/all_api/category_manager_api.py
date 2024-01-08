import datetime
import os
from flask import jsonify, make_response, request
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from application import db

from application.models.category import Category
from application.decorator import admin_required

from ..validation import BadRequest, BusinessValidationError, NotFoundError, UnAuthorizedError
from ..models.user import User
from ..models.role import Role
from werkzeug.security import check_password_hash
from flask_restful import Resource, fields, marshal_with
from ..parser.categoryParser import category_parser



class CategoryManagerAPI(Resource):

    @jwt_required()
    @admin_required
    def post(self, user_id = None):

        errorMessages = []

        current_user_id = get_jwt_identity()
        if user_id is not None and user_id != current_user_id:
            errorMessages.append("Unautorized")
            return UnAuthorizedError(error_messages=errorMessages)
        
        user = User.query.filter_by(id = user_id).first()
        if not user:
            errorMessages.append("User not found")
            return NotFoundError(error_messages=errorMessages)


        input_name = request.form.get("input_name", None)
        input_image = request.files.get("input_image", None)

        if not input_name:
            errorMessages.append("Name cannot be empty")
        elif not input_image:
            errorMessages.append("Image cannot be empty")
        
        if len(errorMessages) != 0:
            raise BusinessValidationError(error_messages=errorMessages)

        category = Category(storedName=input_name, creator=user)
        db.session.add(category)
        db.session.commit()
        # Get the path to the 'src' folder using the current file's path
        current_file_path = os.path.abspath(__file__)
        project_folder_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
        src_folder_path = os.path.join(project_folder_path, 'src/assets/images')

        # Get the filename from the uploaded image
        image_filename = input_image.filename

        # Construct the new image filename with the prefix and serial number
        new_filename = f"category_{category.id}_{image_filename}"

        # Construct the full path to save the image
        image_save_path = os.path.join(src_folder_path, new_filename)
        # Save the image to the full path
        input_image.save(image_save_path)
        category.storedImage= '' + new_filename
        db.session.commit()

        return make_response(jsonify({
                    "message" : "Category created successfully"
                }), 201)
    
    @jwt_required()
    def get(self, user_id = None, category_id = None):
        

        errorMessages = []
        category_list = []

        current_user_id = get_jwt_identity()
        if user_id is not None and user_id != current_user_id:
            errorMessages.append("Unauthorized")
            raise UnAuthorizedError(error_messages=errorMessages)

        user = User.query.filter_by(id=user_id).first()
        if not user:
            errorMessages.append("User not found")
            raise NotFoundError(error_messages=errorMessages)

        if category_id is None:
            if user.role_id == 2:
                categories = user.categories.all()
            else:
                categories = Category.query.all()

            for category in categories:
                category_data = {
                    "id": category.id,
                    "name": category.storedName,
                    "image": category.storedImage,
                    "products": [],
                    "bookings": [],
                    "ratings": []
                }

                for product in category.products_under_category:
                    product_data = {
                        "id": product.id,
                        "name": product.storedName,
                        "price": product.storedPrice,
                        "bookings": [],
                        "ratings": []
                    }

                    for booking in product.bookings:
                        booking_data = {
                            "id": booking.id,
                            "number_of_products": booking.number_of_products,
                            "total_price": booking.total_price,
                            # Add more fields as needed
                        }
                        product_data["bookings"].append(booking_data)

                    for rating in product.ratings:
                        rating_data = {
                            "id": rating.id,
                            "rating": rating.rating,
                            # Add more fields as needed
                        }
                        product_data["ratings"].append(rating_data)

                    category_data["products"].append(product_data)
                
                for booking in category.bookings: 
                    booking_data = {
                        "id": booking.id,
                        "number_of_products": booking.number_of_products,
                        "total_price": booking.total_price
                    }
                    category_data["bookings"].append(booking_data)

                category_list.append(category_data)

            if not category_list:
                errorMessages.append("There are no Categories")
                raise NotFoundError(error_messages=errorMessages)

            return make_response(jsonify({"categories": category_list}), 200)

        else:
            category = Category.query.filter_by(id=category_id).first()
            if not category:
                errorMessages.append("There is no category")
                raise BadRequest(error_messages=errorMessages)
            else:
                category_data = {
                    "id": category.id,
                    "name": category.storedName,
                    "image": category.storedImage,
                    "products": [],
                    "bookings": [],
                    "ratings": []
                }

                for product in category.products_under_category:
                    product_data = {
                        "id": product.id,
                        "name": product.storedName,
                        "price": product.storedPrice,
                        "bookings": [],
                        "ratings": []
                    }

                    for booking in product.bookings:
                        booking_data = {
                            "id": booking.id,
                            "number_of_products": booking.number_of_products,
                            "total_price": booking.total_price,
                            # Add more fields as needed
                        }
                        product_data["bookings"].append(booking_data)

                    for rating in product.ratings:
                        rating_data = {
                            "id": rating.id,
                            "rating": rating.rating,
                        }
                        product_data["ratings"].append(rating_data)

                    category_data["products"].append(product_data)

                for booking in category.bookings:
                    booking_data = {
                        "id": booking.id,
                        "number_of_products": booking.number_of_products,
                        "total_price": booking.total_price
                    }
                    category_data["bookings"].append(booking_data)

                return make_response(jsonify(category_data), 200)

    @jwt_required()
    @admin_required
    def put(self, user_id = None, category_id = None):
        
        errorMessages = []

        current_user_id = get_jwt_identity()
        if user_id is not None and user_id != current_user_id:
            errorMessages.append("Unautorized")
            return UnAuthorizedError(error_messages=errorMessages)

        user = User.query.filter_by(id=user_id).first()
        if not user:
            errorMessages.append("User not found")
            return NotFoundError(error_messages=errorMessages)

        category = Category.query.filter_by(id=category_id).first()
        if not category:
            errorMessages.append("There is no Category")
            raise BadRequest(error_messages=errorMessages)

        input_name = request.form.get("input_name", None)
        input_image = request.files.get("input_image", None)

        if input_name is not None:
            category.storedName = input_name
        

        db.session.commit()

        category_data = {
            "id": category.id,
            "name": category.storedName,
            "image": category.storedImage,
            "products": [],
            "bookings": [],
            "ratings": []
        }

        for product in category.products_under_category:
            product_data = {
                "id": product.id,
                "name": product.storedName,
                "price": product.storedPrice,
                "bookings": [],
                "ratings": []
            }

            for booking in product.bookings:
                booking_data = {
                    "id": booking.id,
                    "number_of_products": booking.number_of_products,
                    "total_price": booking.total_price,
                    # Add more fields as needed
                }
                product_data["bookings"].append(booking_data)

            for rating in product.ratings:
                rating_data = {
                    "id": rating.id,
                    "rating": rating.rating,
                    # Add more fields as needed
                }
                product_data["ratings"].append(rating_data)

            category_data["products"].append(product_data)
        for booking in category.bookings:  # Collect the theatre's bookings
            booking_data = {
                "id": booking.id,
                "number_of_products": booking.number_of_products,
                "total_price": booking.total_price,
                # Add more fields as needed
            }
            category_data["bookings"].append(booking_data)

        return make_response(jsonify(category_data), 200)
    

    @jwt_required()
    @admin_required
    def delete(self, user_id = None, category_id = None):

        errorMessages = []

        current_user_id = get_jwt_identity()
        if user_id is not None and user_id != current_user_id:
            errorMessages.append("Unautorized")
            return UnAuthorizedError(error_messages=errorMessages)
        
        user = User.query.filter_by(id = user_id).first()
        if not user:
            errorMessages.append("User not found")
            return NotFoundError(error_messages=errorMessages)
        
        category = Category.query.filter_by(id = category_id).first()
        if not category:
            errorMessages.append("There is no category")
            raise BadRequest(error_messages=errorMessages)
        else:
            current_file_path = os.path.abspath(__file__)
            project_folder_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
            src_folder_path = os.path.join(project_folder_path, 'src/assets/images')
            image_save_path = os.path.join(src_folder_path, category.storedImage)
            replaced_string = image_save_path.replace("\\", "/")
            
            os.remove(replaced_string)
            db.session.delete(category)
            db.session.commit()
            return make_response(jsonify({"message" : "Category successfully deleted"}), 200)
        
        

