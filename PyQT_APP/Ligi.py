import Ligues
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
# Импортирую классы из программ, чтобы запустить программы
from RussianPL import rpl
from La_Liga import laliga
from Uber_Eats import ligue1
from PremL import PL
from Bundes import bundes
from serieA import SA


class ligue(QtWidgets.QMainWindow, Ligues.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.setWindowTitle('Ligues')

        self.pushButton_9.clicked.connect(self.close)
        self.pushButton_8.clicked.connect(self.rus)
        self.pushButton_2.clicked.connect(self.la)
        self.pushButton_6.clicked.connect(self.Ub)
        self.pushButton.clicked.connect(self.Prem)
        self.pushButton_3.clicked.connect(self.bund)
        self.pushButton_4.clicked.connect(self.sa)

    # создаю функции для открытия окна каждой лиги
    def rus(self):
        self.Rus = rpl()
        self.Rus.show()

    def la(self):
        self.La = laliga()
        self.La.show()

    def Ub(self):
        self.lU = ligue1()
        self.lU.show()

    def Prem(self):
        self.pl = PL()
        self.pl.show()

    def bund(self):
        self.bu = bundes()
        self.bu.show()

    def sa(self):
        self.SERa = SA()
        self.SERa.show()


if __name__ == "__main__":
    a = QtWidgets.QApplication(sys.argv)
    app = ligue()
    app.show()
    a.exec_()
