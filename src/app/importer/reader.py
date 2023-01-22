from typing import Callable, Tuple
from io import TextIOWrapper
import csv

from app.transactions.transaction_model import Transaction


class Reader:
    source: str
    csv_headers: list[str]
    mapping: Callable


def read_data(reader: Reader, filename: str) -> Tuple[list[Transaction], dict]:
    transactions: list[Transaction] = []
    header = {}

    with open(filename, newline="") as csv_file:
        dict_reader = make_dict_reader(csv_file, reader)

        for index, row in enumerate(dict_reader):
            print(row)
            if index == 0:
                header = row
            else:
                row = reader.mapping(row)
                print(row)
                transactions.append(Transaction.from_row(row))

    return transactions, header


def make_dict_reader(csv_file: TextIOWrapper, reader: Reader) -> csv.DictReader:
    return csv.DictReader(
        csv_file,
        fieldnames=reader.csv_headers,
    )
