import os
from argparse import ArgumentParser


def get_arguments() -> ArgumentParser:
    parser = ArgumentParser()
    add_arguments(parser)

    return parser.parse_args()


def add_arguments(parser: ArgumentParser):
    parser.add_argument(
        "-d",
        "--dev",
        help="Runs in development mode",
        action="store_true",
    )
    parser.add_argument(
        "-ro", "--rquestOrigin", help="Sets the allowed request origin", type=str
    )


def get_database_path():
    return os.path.normpath(
        os.path.join(get_root_directory(), "src", "assets", "transactions.db")
    )


def get_mock_database_path():
    return os.path.normpath(
        os.path.join(get_root_directory(), "src", "assets", "mock_transactions.db")
    )


def get_root_directory():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(dir_path, "..", ".."))


args = get_arguments()


class CONFIG:
    DEV: bool = args.dev
    HOST = "0.0.0.0" if not args.dev else None
    DATABASE_PATH = get_database_path()
    MOCK_DATABASE_PATH = get_mock_database_path()
    ROOT_DIR = get_root_directory()
    # REQUEST_ORIGIN: str = args.requestOrigin
    REQUEST_ORIGIN: str = "*"
