from flask import jsonify


def make_not_found_error(request):
    def not_found_error(error):
        message = {
            "status": 404,
            "message": "Record not found: " + request.url,
        }
        respone = jsonify(message)
        respone.status_code = 404
        return respone

    return not_found_error
