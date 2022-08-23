import Seria_A
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class SA(QtWidgets.QMainWindow, Seria_A.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.setWindowTitle('Serie A TIM')

        self.pushButton.clicked.connect(self.close)

if __name__ == "__main__":
    a = QtWidgets.QApplication(sys.argv)
    app = SA()
    app.show()
    a.exec_()