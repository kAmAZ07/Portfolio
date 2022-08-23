import LaLiga
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class laliga(QtWidgets.QMainWindow, LaLiga.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.setWindowTitle('LaLiga')

        self.pushButton.clicked.connect(self.close)


if __name__ == "__main__":
    a = QtWidgets.QApplication(sys.argv)
    app = laliga()
    app.show()
    a.exec_()
