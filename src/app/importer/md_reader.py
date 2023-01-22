from app.importer.reader import Reader


def md_reader():
    reader = Reader()

    reader.source = "moneydashboard"

    reader.csv_headers = [
        "Account",
        "Date",
        "CurrentDescription",
        "OriginalDescription",
        "Amount",
        "L1Tag",
        "L2Tag",
        "L3Tag",
    ]

    reader.mapping = lambda r: r

    return reader
