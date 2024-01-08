from functools import wraps
from flask_jwt_extended import get_jwt_identity
from application.models.user import User
from application.validation import UnAuthorizedError

def manager_required(fn):
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(id=current_user_id).first()

        manager_role_id = 3
        

        if not user or user.role_id != manager_role_id:
            errorMessages = ["Manager access required"]
            return UnAuthorizedError(error_messages=errorMessages)

        return fn(*args, **kwargs)

    return decorated_function