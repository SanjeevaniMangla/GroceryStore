from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from application.models.user import User
from application import db

@jwt_required(optional=True)
def update_last_visited():
    entity = verify_jwt_in_request()
    if entity is not None:
        current_user_id = get_jwt_identity()
        if current_user_id:
            user = User.query.get(current_user_id)
            user.last_visited = datetime.now()
            db.session.commit()