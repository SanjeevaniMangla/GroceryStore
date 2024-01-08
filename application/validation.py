from werkzeug.exceptions import HTTPException
from flask import make_response,jsonify


class NotFoundError(HTTPException):
    def __init__(self, error_messages):
        message = {
            "error_messages":error_messages
        }
        self.response = make_response(jsonify(message), 404)

class BusinessValidationError(HTTPException):
    def __init__(self, error_messages):
        message = {
            "error_messages": error_messages
            }
        self.response = make_response(jsonify(message), 409)

class BadRequest(HTTPException):
    def __init__(self, error_messages):
        message = {
            "error_messages":error_messages
        }
        self.response = make_response(jsonify(message), 400)

class UnAuthorizedError(HTTPException):
    def __init__(self, error_messages):
        message = {
            "error_messages":error_messages
        }
        self.response = make_response(jsonify(message), 401)