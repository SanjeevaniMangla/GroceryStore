import datetime
from flask import jsonify, make_response
from flask_jwt_extended import create_access_token

from ...validation import BusinessValidationError
from ...models.user import User
from ...models.role import Role
from werkzeug.security import check_password_hash
from flask_restful import Resource
from ...parser.loginParser import login_parser

class LoginAPI(Resource):

    def post(self):
        
        args = login_parser.parse_args()
        input_email = args.get("input_email", None)
        input_password = args.get("input_password", None)
        input_role = args.get("input_role", None)
        errorMessages = []

        if not input_email:
            errorMessages.append("Email cannot be empty!")
            raise BusinessValidationError(error_messages=errorMessages)
        elif not input_password:
            errorMessages.append("Password cannot be empty!")
            raise BusinessValidationError(error_messages=errorMessages)
        elif not input_role:
            errorMessages.append("Role cannot be empty!")
            raise BusinessValidationError(error_messages=errorMessages)

        user = User.query.filter(User.stored_email==input_email).first()
        role = Role.query.filter(Role.storedName==input_role).first()
        if user:
            if check_password_hash(user.stored_password, input_password) and user.role_id==role.id:

                # Generate the access token with a 30-minute expiration time
                expires = datetime.timedelta(minutes=60)
                access_token = create_access_token(identity=user.id, expires_delta=expires)
                
                # Get the current time and calculate the expiry time
                now = datetime.datetime.utcnow()
                expiry_time = now + expires
                return make_response(jsonify({
                    "message" : "Logged in successfully!",
                    "id": user.id,
                    "access_token": access_token,
                    "expires": expiry_time
                }), 200)
            elif(check_password_hash(user.stored_password, input_password)):
                errorMessages.append("Chosen role is incorrect!")
                raise BusinessValidationError(error_messages=errorMessages)
            elif user.role_id==role.id:
                errorMessages.append("Password is incorrect!")
                raise BusinessValidationError(error_messages=errorMessages)
            else:
                errorMessages.append("Password is incorrect!")
                errorMessages.append("Chosen role is incorrect!")
                raise BusinessValidationError(error_messages=errorMessages)
        else:
            errorMessages.append("Email id does not exist!")
            raise BusinessValidationError(error_messages=errorMessages)