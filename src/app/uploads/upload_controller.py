from werkzeug.utils import secure_filename
import os

from app.http.request import Request, Error

from app.uploads.filter import UploadFilter
from app.uploads.upload_model import Upload
from app.uploads.config import UPLOAD_FOLDER, MAX_CONTENT_LENGTH


def get_uploads(filter: UploadFilter, request: Request = None) -> list[Upload]:
    return []


def add_upload(request: Request):
    if len(request.files) == 0:
        request.errors.append(resource_not_found_error())
        return

    for file_key in request.files:
        print(file_key)
        file = request.files[file_key]

        print(file)

        save_file(file)


def save_file(file):
    safe_filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, safe_filename))


def resource_not_found_error():
    return Error(
        "No file submitted",
        "No file found in the submitted data",
        400,
    )
