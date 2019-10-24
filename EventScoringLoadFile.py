import argparse
import csv

parser = argparse.ArgumentParser(description='Import a CSV file and place the data in the Event Scoring Database')
parser.add_argument('-f', '--file', default="rider_start.csv",
                    help="CSV file to be entered into the Event Scoring Database")

args = parser.parse_args()

file = args.file
print(file)

with open(file) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'{", ".join(row)}')
            line_count += 1
        print(f'\t{row["number"]} {row["division"]} {row["fenceNumber"]} {row["start"]} {row["finish"]} {row["edit"]}')
        line_count += 1
    print(f'Processed {line_count}')
