import datetime

import jwt
from flask import request, jsonify


def token_required(f):
    from app import app

    def decorated(*args, **kwargs):
        app.logger.info("In decorated token_required")
        token = request.authorization.token
        if not token:
            return jsonify({'error': "Forbidden: 403", "description": 'Token is missing'}), 403
        try:
            jwt.decode(token, app.config['secret_key'], algorithms="HS256")
        except Exception as error:
            app.logger.exception(error)
            return jsonify({'error': "True", "description": 'Token is invalid/expired'}), 401
        return f(*args, **kwargs)
    return decorated


def get_token(auth, ):
    from app import app

    token = jwt.encode({'user': auth.get("username"),
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=10)},
                       app.config['secret_key'], algorithm="HS256")
    return token
