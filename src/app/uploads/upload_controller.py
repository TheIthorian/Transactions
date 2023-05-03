from werkzeug.utils import secure_filename
import os
from datetime import datetime as dt
import hashlib

from app.http.request import Request, Error

from app.uploads.filter import UploadFilter
from app.uploads.upload_model import Upload
from app.uploads.config import UPLOAD_FOLDER

BUF_SIZE = 64 * 1024


def get_uploads(filter: UploadFilter, request: Request = None) -> list[Upload]:
    return []


def add_upload(request: Request):
    if len(request.files) == 0:
        request.errors.append(no_data_provided_error())
        return

    for file_key in request.files:
        file = request.files[file_key]
        if file.filename != "":
            save_file(file)


def save_file(file):
    safe_filename = secure_filename(file.filename)

    file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
    file.save(file_path)

    md5, size = get_file_metadata(file_path)
    new_upload = Upload(
        file_name=safe_filename, size=size, date=dt.now(), md5=md5, status="UPLOADED"
    )
    new_upload.insert()


def get_file_metadata(file_path):
    md5 = hashlib.md5()
    size = 0

    with open(file_path, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            size += len(data)
            if not data:
                break
            md5.update(data)

    return md5.hexdigest(), size


def no_data_provided_error():
    return Error(
        "No file submitted",
        "No file found in the submitted data",
        400,
    )
