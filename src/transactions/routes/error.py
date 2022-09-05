from flask import jsonify, request


def not_found_error(error):
    message = {
        "status": 404,
        "message": "Record not found: " + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
