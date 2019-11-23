import sys
import datetime
import sqlite3
from PyQt5 import QtWidgets, uic
from dbHelper import DbHelper
from results import Results


# open and connect to database
def opendatabase(filename, db):
    db.setDatabaseFile(filename)
    db.connectToDatabase()
    db.openDatabaseFileRead()

def converttime(millsecs):
    time = datetime.datetime.fromtimestamp(millsecs/1000)
    return time

def loaddata(db, window):
    if db.counttablerows('xcResultTable') <= 0:
        return False
    else:
        riders = db.selectFromTable('SELECT * FROM xcResultTable')

        for row_number,rider in enumerate(riders):
            window.tableWidget.insertRow(row_number)
            window.tableWidget.setItem(row_number, 0, QtWidgets.QTableWidgetItem(str(rider[0])))
            window.tableWidget.setItem(row_number, 1, QtWidgets.QTableWidgetItem(str(rider[1])))
            window.tableWidget.setItem(row_number, 2, QtWidgets.QTableWidgetItem(str(converttime(rider[2]))))
            window.tableWidget.setItem(row_number, 3, QtWidgets.QTableWidgetItem(str(converttime(rider[3]))))
            window.tableWidget.setItem(row_number, 4, QtWidgets.QTableWidgetItem(str(rider[4])))
            window.tableWidget.setItem(row_number, 5, QtWidgets.QTableWidgetItem(str(rider[5])))
            window.tableWidget.setItem(row_number, 6, QtWidgets.QTableWidgetItem(str(rider[6])))
            window.tableWidget.setItem(row_number, 7, QtWidgets.QTableWidgetItem(str(rider[7])))
            window.tableWidget.setItem(row_number, 8, QtWidgets.QTableWidgetItem(str(rider[8])))
            window.tableWidget.setItem(row_number, 9, QtWidgets.QTableWidgetItem(str(rider[9])))

def processdata(db, window):
    try:
        result = Results()
        result.processresults()
        loaddata(db, window)
    except sqlite3.DatabaseError as error:
        print("xcResultTable Table already exists", " ", error.args[0])

# Setup Application
def main():
    app = QtWidgets.QApplication([])
    window = uic.loadUi('test.ui')

    db = DbHelper()
    try:
        opendatabase('event.db', db)
    except sqlite3.DatabaseError as error:
        print("Cannot connect to Database ", DbHelper.riderDbFile, " ", error.args[0])

    loaddata(db, window)
    window.processData.clicked.connect(lambda: processdata(db, window))
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()