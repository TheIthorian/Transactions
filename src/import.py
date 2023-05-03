from argparse import ArgumentParser
import os

from util.dir import get_root_directory
from app import config
from app.importer.register import Register, register_readers
from app.importer.reader import read_data
from app.importer.importer import insert_transactions

MONEY_DASHBOARD = "moneydashboard"


def get_parser(register: Register) -> ArgumentParser:
    parser = ArgumentParser("importer")
    supported_sources = register.get_sources()
    sources_as_string = ", ".join(supported_sources)

    parser.add_argument(
        "-f",
        "--filename",
        help="Sets the filename of the transactions to import",
        type=str,
        default="new_Transactions.csv",
        required=False,
    )

    parser.add_argument(
        "-s",
        "--source",
        help=f"Sets the source of the transactions. Supported options are: [{sources_as_string}]",
        type=str,
        default=MONEY_DASHBOARD,
        choices=supported_sources,
        required=False,
    )

    parser.add_argument(
        "-a", "--account", help="Sets which account to use", type=str, default=""
    )

    return parser


if __name__ == "__main__":
    register = register_readers()

    parser = get_parser(register)
    args = parser.parse_args()

    reader = register.get_reader(args.source)
    if reader is None:
        raise f"Reader for {args.source} not found!"

    filename = os.path.normpath(os.path.join(get_root_directory(), args.filename))
    new_transactions, _ = read_data(reader, filename)

    config.init(True, args.account)
    insert_transactions(new_transactions)
