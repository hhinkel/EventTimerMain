import sys
import datetime
import sqlite3
from PyQt5 import QtWidgets, uic
from dbHelper import DbHelper
from results import Results
from division import Division


# open and connect to database
def opendatabase(filename, db):
    db.setDatabaseFile(filename)
    db.connectToDatabase()
    db.openDatabaseFileAppend()


def converttime(millsecs):
    return datetime.datetime.fromtimestamp(millsecs / 1000)


def getminoncourse(secs):
    return str(datetime.timedelta(seconds=secs))


def loaddata(window):
    db = DbHelper()
    opendatabase('event.db', db)
    riders = db.selectFromTable('SELECT * FROM xcResultTable')

    for row_number,rider in enumerate(riders):
        window.tableWidget.insertRow(row_number)
        window.tableWidget.setItem(row_number, 0, QtWidgets.QTableWidgetItem(str(rider[0])))
        window.tableWidget.setItem(row_number, 1, QtWidgets.QTableWidgetItem(str(rider[1])))
        window.tableWidget.setItem(row_number, 2, QtWidgets.QTableWidgetItem(str(converttime(rider[2]))))
        window.tableWidget.setItem(row_number, 3, QtWidgets.QTableWidgetItem(str(converttime(rider[3]))))
        if rider[4] is None:
            window.tableWidget.setItem(row_number, 4, QtWidgets.QTableWidgetItem('None'))
        else:
            window.tableWidget.setItem(row_number, 4, QtWidgets.QTableWidgetItem(str(getminoncourse(int(rider[4])))))
        window.tableWidget.setItem(row_number, 5, QtWidgets.QTableWidgetItem(str(rider[5])))
        window.tableWidget.setItem(row_number, 6, QtWidgets.QTableWidgetItem(str(rider[6])))
        window.tableWidget.setItem(row_number, 7, QtWidgets.QTableWidgetItem(str(rider[7])))
        window.tableWidget.setItem(row_number, 8, QtWidgets.QTableWidgetItem(str(rider[8])))
        window.tableWidget.setItem(row_number, 9, QtWidgets.QTableWidgetItem(str(rider[9])))

    db.closeDatabaseFile()


def counttablerows():
    db = DbHelper()
    opendatabase('event.db', db)
    rows = db.counttablerows('xcResultTable')
    db.closeDatabaseFile()
    return rows


def processdata(window):
    try:
        result = Results()
        result.processresults()
    except sqlite3.DatabaseError as error:
        print("xcResultTable Table already exists", " ", error.args[0])
    loaddata(window)

# Setup Application
def main():
    div = Division()
    div.setupdivision()
    app = QtWidgets.QApplication([])
    window = uic.loadUi('test.ui')

    if counttablerows() > 0:
        loaddata(window)

    window.processData.clicked.connect(lambda: processdata(window))
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()