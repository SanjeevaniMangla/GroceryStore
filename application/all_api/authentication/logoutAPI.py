from flask import jsonify, make_response
from flask_jwt_extended import get_jwt, jwt_required

from application.blocklist import BLOCKLIST
from flask_restful import Resource


# API for user logout
class LogoutAPI(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return make_response(jsonify({
            "message": "You are successfully logged out!!"
        }), 200)