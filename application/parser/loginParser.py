from flask_restful import reqparse

login_parser = reqparse.RequestParser()
login_parser.add_argument('input_email')
login_parser.add_argument('input_password')
login_parser.add_argument('input_role')