from flask import jsonify, make_response
from flask_jwt_extended import jwt_required
from application.models.category import Category
from application.decorator import admin_required
from flask_restful import Resource

class GenerateCsvAPI(Resource):

    @jwt_required()
    @admin_required
    def get(self, user_id, category_id):

        category = Category.query.filter_by(id = category_id).first()
        all_products = category.products_under_category

        products_list = []
        for product in all_products:
            product_data = {
                "id": product.id,
                "storedName": product.storedName,
                
            }
            products_list.append(product_data)

        from application.tasks import generate_csv
        a = generate_csv.delay(category_id=category.id, category_name=category.storedName, products=products_list)
        return make_response(jsonify({
            "Task_ID" : a.id
            }), 200)