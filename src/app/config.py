import json
import os
from argparse import ArgumentParser

from util.dir import get_root_directory

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

    parser.add_argument(
        "-a", "--account", help="Sets the account name", type=str, default=""
    )


def get_database_path(db_name: str):
    return os.path.normpath(
        os.path.join(get_root_directory(), "src", "assets", db_name)
    )


def get_config():
    file_path = os.path.join(get_root_directory(), "config.json")
    config = {}
    with open(file_path) as config_file:
        config = json.load(config_file)
    return config


class Config:
    def __init__(self):
        pass

    def set_values(self, args, config):
        self.DEV: bool = args.dev or False
        self.DEMO: bool = args.demo or False

        self.API_KEY: str = config["API_KEY"]
        self.PASSWORD: str = config["PASSWORD"]
        self.HOST: str = config["HOST"] if not args.dev else None
        self.REQUEST_ORIGIN: str = config["REQUEST_ORIGIN"]

        self.ROOT_DIR: str = get_root_directory()

        account = args.account if args.account else ""
        self.PROD_DATABASE_PATH: str = get_database_path(account + DATABASE_NAME)
        self.MOCK_DATABASE_PATH: str = get_database_path(MOCK_DATABASE_NAME)
        self.DEMO_DATABASE_PATH: str = get_database_path(DEMO_DATABASE_NAME)
        self.DATABASE_PATH: str = self.PROD_DATABASE_PATH

        self.PRINT_QUERIES: bool = config["PRINT_QUERIES"]


CONFIG = Config()


def init(ignore_parser: bool = False, account: str = None):
    class DefaultArgs:
        dev = False
        demo = False
        account = ""

    args = DefaultArgs()
    if not ignore_parser:
        args = get_arguments()
        if args.demo:
            print("Currently running on demo environment")

    if account is not None:
        args.account = account

    config = get_config()
    CONFIG.set_values(args, config)
