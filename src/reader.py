"""Functions to read and write data to the os.

(C) 2022, TheIthorian, United Kingdom
"""

import csv
from data import Transaction


def read_data():
    data = []
    header = {}
    file = "Transactions.csv"

    with open(file, newline="") as csv_file:
        reader = csv.DictReader(
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
        for index, row in enumerate(reader):
            if index == 0:
                header = row
            else:
                data.append(Transaction.from_row(row))

    return header, data
