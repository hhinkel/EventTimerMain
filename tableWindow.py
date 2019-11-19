from PyQt5 import QtWidgets
from table import Ui_MainWindow


class tablewindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(tablewindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.setRowCount(4)
        self.ui.pushButton.clicked.connect(self.clear)

    def clear(self):
        self.ui.tableWidget.clear()
