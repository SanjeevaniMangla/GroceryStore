from datetime import datetime
import os
from flask import jsonify, make_response, request
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from application import db
from application.models.product import Product

from application.models.category import Category
from application.decorator import admin_required

from ..validation import BadRequest, BusinessValidationError, NotFoundError, UnAuthorizedError
from ..models.user import User
from ..models.role import Role
from werkzeug.security import check_password_hash
from flask_restful import Resource, fields, marshal_with



class SearchCategoryAPI(Resource):

    @jwt_required()
    def get(self, user_id = None):
                
        input_name = request.args.get('input_name')
        
        searched_categories = []

        if input_name:
            searched_categories = Category.query.filter(
                Category.storedName.like(input_name + '%'),
            ).all()
        else:
            searched_categories = Category.query.all()

        category_list = []
        for category in searched_categories:
            category_data = {
                "id": category.id,
                "name": category.storedName,
                "image": category.storedImage
            }
            category_list.append(category_data)

        return make_response(jsonify({"categories": category_list}), 200)
    