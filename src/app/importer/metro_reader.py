from app.importer.reader import Reader


def metro_reader():
    reader = Reader()

    reader.source = "metro"

    reader.csv_headers = [
        "Date",
        "Details",
        "Transaction Type",
        "In",
        "Out",
        "Balance",
        "l1",
        "l2",
        "l3",
    ]

    reader.mapping = convert_to_md_format

    return reader


def convert_to_md_format(row: dict[str, str]):
    [day, month, year] = row["Date"].split("/")
    date = "-".join([year, month, day])

    new_row = {}
    new_row["Account"] = "Metro"
    new_row["Date"] = date
    new_row["CurrentDescription"] = ""
    new_row["OriginalDescription"] = row["Details"]
    new_row["Amount"] = row["In"] if row["In"] != "" else "-" + row["Out"]
    new_row["L1Tag"] = row["l1"]
    new_row["L2Tag"] = row["l2"]
    new_row["L3Tag"] = row["l3"]

    return new_row
