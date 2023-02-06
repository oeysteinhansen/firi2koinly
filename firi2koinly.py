
import csv
import sys
import datetime
from dateutil import parser


def main():
    #filename = sys.argv[1]
    filename = "Firi - Transaksjoner 2022.csv"
    out_file = "Koinly.csv"

    data_rows = []

    with open(file=filename, mode="r", newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            data = {}
            for k, v in row.items():
                data[str(k)]=v
            data_rows.append(data)

    # Change data
    for row in data_rows:
        # Rename the Colom from Action to Label
        row["Label"] = row["Action"]
        del row["Action"]
        # Rename and format to Koinly Date
        created_date = row["Created at"]
        created_date = created_date.replace(" GMT+0000 (Coordinated Universal Time)", "+00:00")
        created_date = parser.parse(created_date)
        created_date = created_date.isoformat(sep=" ", timespec="seconds")
        created_date = created_date.replace("+00:00", " UTC")
        row["Koinly Date"] = created_date
        del row["Created at"]


    with open(out_file, mode='w') as out_csvfile:
        fieldnames = [
            "Transaction ID",
            "Match ID",
            "Withdraw ID",
            "Deposit ID",
            "Withdraw address",
            "Withdraw transaction ID",
            "Deposit address",
            "Deposit transaction ID",
            "Label",
            "Currency",
            "Amount",
            "Koinly Date"
        ]
        writer = csv.DictWriter(out_csvfile, fieldnames)

        for row in data_rows:
            # Grab only fileds pressent in the output.
            new_row = {}
            for field in fieldnames:
                new_row[field] = row[field]
            writer.writerow(new_row)

main()