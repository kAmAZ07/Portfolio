import Enterance
# Импортирую классы из программ Play и Ligi
from Play import ADD
from Ligi import ligue
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Main(QtWidgets.QMainWindow, Enterance.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.setWindowTitle('Football browser')

        # Задаю команды кнопкам
        self.pushButton.clicked.connect(self.Finder_players)
        self.pushButton_2.clicked.connect(self.Ligues_commands)

# Создаю функцию открывающую класс ADD и запускающую программу Play
    def Finder_players(self):
        self.find_players = ADD()
        self.find_players.show()

# Создаю функцию открывающую класс ligue и запускающую программу Ligi
    def Ligues_commands(self):
        self.Ligues = ligue()
        self.Ligues.show()


if __name__ == "__main__":
    a = QtWidgets.QApplication(sys.argv)
    app = Main()
    app.show()
    a.exec_()
