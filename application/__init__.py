from datetime import datetime
from flask import Flask, request, redirect
from flask import render_template
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required, verify_jwt_in_request
from application.validation import UnAuthorizedError
from application.blocklist import BLOCKLIST

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    CORS(app, origins=['http://localhost:8080'])
    
            
    app.config['SECRET_KEY'] = "gveghwcjmijlmrkb"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['JWT_SECRET_KEY'] = 'something-is-secret'  
    app.config['CORS_SUPPORTS_CREDENTIALS'] = True
    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)

    from application.jwt_token import check_if_token_in_blocklist, revoked_token_callback
    jwt.token_in_blocklist_loader(check_if_token_in_blocklist)
    jwt.revoked_token_loader(revoked_token_callback)

    from application.all_api.authentication.loginAPI import LoginAPI
    from application.all_api.authentication.logoutAPI import LogoutAPI
    from application.all_api.authentication.signupAPI import SignUpAPI
    from application.all_api.role_api import RoleAPI
    from application.all_api.category_api import CategoryAPI   
    from application.all_api.category_manager_api import CategoryManagerAPI   
    from application.all_api.product_api import ProductAPI
    from application.all_api.product_manager_api import ProductManagerAPI
    from application.all_api.booking_api import BookingAPI
    from application.all_api.search_category_api import SearchCategoryAPI
    from application.all_api.search_product_api import SearchProductAPI
    from application.all_api.celery_tasks_api import CeleryTaskAPI
    from application.all_api.generate_csv_api import GenerateCsvAPI
    from application.all_api.download_csv_api import DownloadCsvAPI
    from application.all_api.ratings_api import RatingsAPI
    from application.all_api.summary_api import SummaryAPI

    api.add_resource(LoginAPI, "/login")
    api.add_resource(SignUpAPI, "/signup")
    api.add_resource(RoleAPI, "/api/roles")
    api.add_resource(CategoryAPI, "/user/<int:user_id>/category_api", "/user/<int:user_id>/category_api/<int:category_id>", "/category_api")
    api.add_resource(CategoryManagerAPI, "/user/<int:user_id>/category_manager_api", "/user/<int:user_id>/category_manager_api/<int:category_id>", "/category_manager_api")
    api.add_resource(ProductAPI, "/user/<int:user_id>/category/<int:category_id>/product_api",
                     "/user/<int:user_id>/category/<int:category_id>/product_api/<int:product_id>")
    api.add_resource(ProductManagerAPI, "/user/<int:user_id>/category/<int:category_id>/product_manager_api",
                     "/user/<int:user_id>/category/<int:category_id>/product_manager_api/<int:product_id>")
    api.add_resource(LogoutAPI, "/logout")
    api.add_resource(BookingAPI, "/user/<int:user_id>/category/<int:category_id>/product/<int:product_id>/booking_api", "/user/<int:user_id>/booking_api")
    api.add_resource(SearchCategoryAPI, "/search/user/<int:user_id>/categories")    
    api.add_resource(SearchProductAPI, "/search/user/<int:user_id>/products")
    api.add_resource(CeleryTaskAPI, "/user/<int:user_id>/check-state/<string:task_id>")
    api.add_resource(GenerateCsvAPI, "/user/<int:user_id>/category/<int:category_id>/generate-csv")
    api.add_resource(DownloadCsvAPI, "/user/<int:user_id>/download-file")
    api.add_resource(RatingsAPI, "/user/<int:user_id>/category/<int:category_id>/product/<int:product_id>/booking/<int:booking_id>/rating_api")
    api.add_resource(SummaryAPI, "/user/<int:user_id>/category/<int:category_id>/summary_api")

    from .models.user import User
    from .models.role import Role
    from .models.product import Product
    from .models.category import Category
    from .models.product_category import ProductCategoryAssociation
    from .models.booking import Booking
    from .models.rating import Rating
    
    from application.last_visited_user import update_last_visited


    @app.before_request
    def before_request_callback():
        excluded_endpoints = ['roleapi','loginapi', 'signupapi']
        if request.endpoint not in excluded_endpoints:
            update_last_visited()

    with app.app_context():
        create_database()
        add_initial_roles()
    return app


def create_database():
    if not path.exists("websites/" + DB_NAME):
        db.create_all()
        
def add_initial_roles():
    from .models.role import Role

    # Check if the role table is empty
    if Role.query.count() == 0:
        # Add the initial roles
        user_role = Role(id=1, storedName='User')
        admin_role = Role(id=2, storedName='Admin')
        manager_role = Role(id=3, storedName='Manager')

        db.session.add(user_role)
        db.session.add(admin_role)
        db.session.add(manager_role)
        db.session.commit()