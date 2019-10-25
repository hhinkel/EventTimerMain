import argparse
import csv

from rider import Rider
from setup import Setup
from dbHelper import DbHelper


def parsearguments():
    parser = argparse.ArgumentParser(description='Import a CSV file and place the data in the Event Scoring Database')
    parser.add_argument('-f', '--file', required=True,
                        help="CSV file to be entered into the Event Scoring Database")
    args = parser.parse_args()
    return args.file


def setuptables(file):
    db = DbHelper()
    db.createdatabase(file)


def setuprider(entry, r):
    r.number = int(entry["number"])
    r.division = entry["division"]
    r.fence = int(entry["fenceNumber"])
    r.startTime = int(entry["start"])
    r.finishTime = int(entry["finish"])
    if entry["edit"]:
        r.edit = entry["edit"]
    else:
        r.edit = 'null'


setupFile = "setup.json"
setup = Setup(setupFile)
setuptables(setup.databaseFile)

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
        rider.updateTables(setup.databaseFile)
        print(f'\t{rider.number} {rider.division} {rider.fence} {rider.startTime} {rider.finishTime} {rider.edit}')
        line_count += 1
    print(f'Processed {line_count}')
