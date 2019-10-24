import argparse
import csv

from rider import Rider

def parsearguments():
    parser = argparse.ArgumentParser(description='Import a CSV file and place the data in the Event Scoring Database')
    parser.add_argument('-f', '--file', default="rider_start.csv",
                        help="CSV file to be entered into the Event Scoring Database")

    args = parser.parse_args()

    return args.file

def setuprider(entry, r):
    r.number = entry["number"]
    r.division = entry["division"]
    r.fence = entry["fenceNumber"]
    r.startTime = entry["start"]
    r.finishTime = entry["finish"]
    r.edit = entry["edit"]


file = parsearguments()
print(file)

with open(file) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'{", ".join(row)}')
            line_count += 1
        rider = Rider(None)
        setuprider(row, rider)
        print(f'\t{rider.number} {rider.division} {rider.fence} {rider.startTime} {rider.finishTime} {rider.edit}')
        line_count += 1
    print(f'Processed {line_count}')
