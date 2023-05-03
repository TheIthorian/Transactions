import os
from app.importer.reader import read_data
from app.importer.importer import insert_transactions
from app.importer.register import register_readers

from app.uploads.upload_model import Upload
from app.uploads.config import UPLOAD_FOLDER


def process_file(file_upload: Upload, reader_source: str = "moneydashboard"):
    register = register_readers()
    reader = register.get_reader(reader_source)
    if reader is None:
        raise f"Reader for {reader_source} not found!"

    filename = os.path.join(UPLOAD_FOLDER, file_upload.file_name)
    new_transactions, _ = read_data(reader, filename)

    # insert_transactions(new_transactions)

    # for t in new_transactions:
    #     print(t)

    file_upload.status = "COMPLETE"
    file_upload.update()
