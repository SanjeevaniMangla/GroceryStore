from flask_restful import reqparse


category_parser = reqparse.RequestParser()
category_parser.add_argument('input_name')
category_parser.add_argument('input_image')