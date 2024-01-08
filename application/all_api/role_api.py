from application.models.role import Role
from flask_restful import Resource, fields, marshal_with


class MyDateFormat(fields.Raw):
    def format(self, value):
        return value.strftime("%d-%m-%Y %H:%M:%S")


output_role_fields = {
    "id": fields.Integer,
    "storedName" : fields.String,
}

# blog_parser = reqparse.RequestParser()
# blog_parser.add_argument('input_title')
# blog_parser.add_argument('input_caption')

class RoleAPI(Resource):
    # Get user
    @marshal_with(output_role_fields)
    def get(self):
        roles = Role.query.all()
        return roles