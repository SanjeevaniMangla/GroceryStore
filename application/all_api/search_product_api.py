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



class SearchProductAPI(Resource):

    @jwt_required()
    def get(self, user_id = None):
                
        input_name = request.args.get('input_name')
        input_price = request.args.get('input_price')
        searched_shows = []

        if input_name:
            searched_products = Product.query.filter(
                Product.storedName.like(input_name + '%'),
            ).all()
        elif input_price:
            searched_products = Product.query.filter(
                Product.storedPrice.like(input_price + '%'),
            ).all()

        else:
            searched_products = Product.query.all()

        product_list = []
        for product in searched_products:
            product_data = {
                "id": product.id,
                "name": product.storedName,
                "price": product.storedPrice,
            }
            product_list.append(product_data)

        return make_response(jsonify({"products": product_list}), 200)