from application.blocklist import BLOCKLIST
from application.validation import UnAuthorizedError

errorMessages = []


def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST
    
    
def revoked_token_callback(jwt_header, jwt_payload):
    errorMessages.append("You are logged out!!")
    raise UnAuthorizedError(error_messages=errorMessages)

