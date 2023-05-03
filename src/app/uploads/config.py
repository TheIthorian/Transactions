import os
from app.util import dir


UPLOAD_FOLDER = os.path.join(dir.get_root_directory(), "uploads")
MAX_CONTENT_LENGTH = 16 * 1000 * 1000
