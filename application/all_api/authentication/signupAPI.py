import datetime
from flask import jsonify, make_response
from application.models.role import Role

from application.validation import BadRequest, BusinessValidationError
from application import db
from ...models.user import User
from werkzeug.security import generate_password_hash
from flask_restful import Resource
from ...parser.signUpParser import signup_parser


# API for user sign-up
class SignUpAPI(Resource):
    def post(self):

        args = signup_parser.parse_args()
        input_email = args.get("input_email", None)
        input_password = args.get("input_password", None)
        input_username = args.get("input_username", None)
        input_role = args.get("input_role", None)
        error_messages =[]
        # Input fields empty validation
        if not input_email:
            error_messages.append("Email cannot be empty")
        elif not input_username:
            error_messages.append("Username cannot be empty")
        elif not input_password:
            error_messages.append("Password cannot be empty")
        elif not input_role:
            error_messages.append("Role cannot be empty")
        
        if len(error_messages) != 0:
            raise BusinessValidationError(error_messages=error_messages)
            
        
        # More validations
        email_exists = User.query.filter(User.stored_email==input_email).first()
        username_exists = User.query.filter(User.stored_username==input_username).first()
        
        if email_exists:
            error_messages.append(input_email + " is already registered with us. Try to use different email")
        if username_exists:
            error_messages.append(input_username + " is already registered with us. Try to use different username")
        if len(input_username) < 2:
            error_messages.append('Username length should be atleast 2')
        if len(input_password) < 6:
            error_messages.append('Password length should be atleast 6')
        if len(input_email) < 4:
            error_messages.append('Email address is invalid')

        
        if len(error_messages) != 0:
            raise BusinessValidationError(error_messages=error_messages)
        else:
            inputRole = Role.query.filter(Role.storedName==input_role).first()
            new_user = User(stored_email = input_email, stored_username = input_username, stored_password = generate_password_hash(input_password),
                             role_id = inputRole.id)
            
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify({
                'message' : 'Account has been successfully created',
                
            }),201)