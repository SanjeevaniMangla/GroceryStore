from flask_restful import reqparse

product_parser = reqparse.RequestParser()
product_parser.add_argument('input_name')
product_parser.add_argument('input_price')
