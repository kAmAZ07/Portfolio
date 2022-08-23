import Ligue_1_Uber_Eats
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class ligue1(QtWidgets.QMainWindow, Ligue_1_Uber_Eats.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.setWindowTitle('Ligue 1 Uber Eats')

        self.pushButton.clicked.connect(self.close)


if __name__ == "__main__":
    a = QtWidgets.QApplication(sys.argv)
    app = ligue1()
    app.show()
    a.exec_()
