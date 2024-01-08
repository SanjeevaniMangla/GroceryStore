from flask import send_file
from flask_jwt_extended import jwt_required
from application.decorator import admin_required
from flask_restful import Resource

class DownloadCsvAPI(Resource):

    @jwt_required()
    @admin_required
    def get(self, user_id):
        return send_file("static/data.csv", as_attachment=True, mimetype='text/csv')