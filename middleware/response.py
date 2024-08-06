import json

from flask import jsonify, request

from middleware.constants import UIUrls


def register_middleware(app):
    @app.after_request
    def format_response(response):
        if set(request.url.split("/")).intersection(set(UIUrls.BY_PASS_URL.value)):
            return response

        if response.is_json:
            return response

        response_data = response.get_data(as_text=True)
        try:
            data = {
                "error": False,
                "data": json.loads(response_data)
            }
        except ValueError:
            data = {
                "error": False,
                "data": response_data
            }

        response_data = jsonify(data)
        response_data.status_code = response.status_code
        return response_data

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.exception(e)
        response = {
            "error": str(e),
            "description": getattr(e, 'description', 'No description available')
        }
        return jsonify(response), getattr(e, 'code', 500)

    return app
