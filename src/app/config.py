import json
import os
from argparse import ArgumentParser

DATABASE_NAME = "transactions.db"
MOCK_DATABASE_NAME = "mock_transactions.db"
DEMO_DATABASE_NAME = "demo_transactions.db"


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
        "--demo",
        help="Runs in demo mode which uses fake data",
        action="store_true",
    )


def get_database_path(db_name: str):
    return os.path.normpath(
        os.path.join(get_root_directory(), "src", "assets", db_name)
    )


def get_root_directory():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(dir_path, "..", ".."))


def get_config():
    file_path = os.path.join(get_root_directory(), "config.json")
    config = {}
    with open(file_path) as config_file:
        config = json.load(config_file)
    return config


args = get_arguments()
if args.demo:
    print("Currently running on demo environment")

config = get_config()


class CONFIG:
    DEV: bool = args.dev
    DEMO: bool = args.demo

    API_KEY: str = config["API_KEY"]
    PASSWORD: str = config["PASSWORD"]
    HOST: str = config["HOST"] if not args.dev else None
    REQUEST_ORIGIN: str = config["REQUEST_ORIGIN"]

    ROOT_DIR: str = get_root_directory()
    PROD_DATABASE_PATH: str = get_database_path(DATABASE_NAME)
    MOCK_DATABASE_PATH: str = get_database_path(MOCK_DATABASE_NAME)
    DEMO_DATABASE_PATH: str = get_database_path(DEMO_DATABASE_NAME)
    DATABASE_PATH = PROD_DATABASE_PATH

    PRINT_QUERIES: bool = config["PRINT_QUERIES"]
