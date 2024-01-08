from flask_restful import reqparse

rating_parser = reqparse.RequestParser()
rating_parser.add_argument('rating')