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


def make_filesize_too_large_error(request):
    def filesize_too_large_error(error=None):
        message = {
            "status": 413,
            "message": "File too large",
        }
        respone = jsonify(message)
        respone.status_code = 413
        return respone

    return filesize_too_large_error
