from flask_restful import reqparse

signup_parser = reqparse.RequestParser()
signup_parser.add_argument('input_email')
signup_parser.add_argument('input_username')
signup_parser.add_argument('input_password')
signup_parser.add_argument('input_confirm_password')
signup_parser.add_argument('input_role')