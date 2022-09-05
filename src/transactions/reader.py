"""Functions to read and write data to the os.

(C) 2022, TheIthorian, United Kingdom
"""

import csv
from io import TextIOWrapper
from typing import Tuple

from transactions.data import Transaction


def read_data(filename: str) -> Tuple[dict, list[Transaction]]:
    transactions: list[Transaction] = []
    header = {}

    with open(filename, newline="") as csv_file:
        reader = make_dict_reader(csv_file)

        for index, row in enumerate(reader):
            if index == 0:
                header = row
            else:
                transactions.append(Transaction.from_row(row))

    return header, transactions  # Swap these


def make_dict_reader(csv_file: TextIOWrapper):
    return csv.DictReader(
        csv_file,
        fieldnames=[
            "Account",
            "Date",
            "CurrentDescription",
            "OriginalDescription",
            "Amount",
            "L1Tag",
            "L2Tag",
            "L3Tag",
        ],
    )
