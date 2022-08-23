import Bundesliga
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class bundes(QtWidgets.QMainWindow, Bundesliga.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.setWindowTitle('Bundesliga')

        self.pushButton.clicked.connect(self.close)


if __name__ == "__main__":
    a = QtWidgets.QApplication(sys.argv)
    app = bundes()
    app.show()
    a.exec_()