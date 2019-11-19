import sys
from PyQt5 import QtWidgets, QtSql, QtCore
from tableWindow import tablewindow


def createConnection():
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('event.db')
    return db


def initializeModel(model):
    model = QtSql.QSqlTableModel()
    model.setTable('xcResultTable')
    model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
    model.select()

    model.setHeaderData(0, QtCore.Qt.Horizontal, 'Rider Number')
    model.setHeaderData(1, QtCore.Qt.Horizontal, 'Division')
    model.setHeaderData(2, QtCore.Qt.Horizontal, 'Time On Course')


def createView(title, model):
    view = QtWidgets.QTableView()
    view.setModel(model)
    view.setWindowTitle(title)
    return view


def main():
    app = QtWidgets.QApplication([])
    db = createConnection()
    ok = db.open()
    if not ok:
        sys.exit(15)
    model = QtSql.QSqlTableModel()
    initializeModel(model)

    view = createView('Tabel Model (View 1)', model)
    view.show()

    application = tablewindow()
    application.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()