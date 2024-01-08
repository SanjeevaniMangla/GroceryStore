from flask_restful import reqparse

booking_parser = reqparse.RequestParser()
booking_parser.add_argument('number_of_products')
booking_parser.add_argument('total_price')