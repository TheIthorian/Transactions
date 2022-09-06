from argparse import ArgumentParser
import os


def add_arguments(parser):
    parser.add_argument(
        "-d", "--dev", help="Runs in development mode", action="store_true"
    )


def get_arguments() -> ArgumentParser:
    parser = ArgumentParser()
    add_arguments(parser)

    return parser.parse_args()


def get_database_path():
    return os.path.join(get_root_directory(), "src", "assets", "transactions.db")


def get_root_directory():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dir_path, "..", "..")


args = get_arguments()


class CONFIG:
    DEV = args.dev
    HOST = "0.0.0.0" if not args.dev else None
    DATABASE_PATH = get_database_path()
    ROOT_DIR = get_root_directory()
