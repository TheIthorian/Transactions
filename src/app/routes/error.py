from flask import jsonify


def make_not_found_error(request):
    def not_found_error(error=None):
        message = {
            "status": 404,
            "message": str(error),
        }
        respone = jsonify(message)
        respone.status_code = 404
        return respone

    return not_found_error
