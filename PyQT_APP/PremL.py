import PremierLigue
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class PL(QtWidgets.QMainWindow, PremierLigue.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.setWindowTitle('Premier Ligue')

        self.pushButton.clicked.connect(self.close)

if __name__ == "__main__":
    a = QtWidgets.QApplication(sys.argv)
    app = PL()
    app.show()
    a.exec_()