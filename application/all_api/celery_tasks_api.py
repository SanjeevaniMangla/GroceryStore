from flask import jsonify, make_response
from flask_jwt_extended import jwt_required
from application.decorator import admin_required
from flask_restful import Resource

class CeleryTaskAPI(Resource):

    @jwt_required()
    @admin_required
    def get(self, user_id, task_id):
        from main import celery
        res = celery.AsyncResult(task_id)
        
        return make_response(jsonify({
            "Task_ID" : res.id,
            "Task_State": res.state,
            "Task_Result": res.result
            }), 200)