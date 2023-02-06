
import csv
import sys
import datetime
from dateutil import parser


def firi_to_koinly_csv(input_filename, output_filename):
    """ Convert the CSV from Firi export, to a supported Koinly CSV input format. """
    data_rows = []

    # Load input CSV file - Firi
    with open(file=input_filename, mode="r", newline='') as csvfile:
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

    # Write output CSV file - Koinly
    with open(output_filename, mode='w') as out_csvfile:
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
        writer.writeheader()

        for row in data_rows:
            # Grab only fileds pressent in the output.
            new_row = {}
            for field in fieldnames:
                new_row[field] = row[field]
            writer.writerow(new_row)

def main():
    import argparse
    import pathlib
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', help='Input filename', required=True)
    parser.add_argument('-o','--output', help='Output filename (is generated from input when omited)', required=False)
    args = parser.parse_args()

    input_filename = args.input
    output_filename = args.output

    if pathlib.Path(input_filename).exists() is False:
        print(f"Input file does not exist: '{input_filename}'")
        sys.exit(-1)

    if output_filename is None:
        output_filename = input_filename + ".koinly.csv"


    firi_to_koinly_csv(input_filename, output_filename)


main()