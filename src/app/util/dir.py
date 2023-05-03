import os


def get_root_directory():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(dir_path, "..", ".."))
