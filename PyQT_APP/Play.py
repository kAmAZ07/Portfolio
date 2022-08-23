import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtWidgets import QMessageBox, QTableView, QApplication, QWidget
import Find_players
import sys
from PyQt5.QtCore import QCoreApplication


class ADD(QtWidgets.QMainWindow, Find_players.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.textEdit.clear()
        self.setWindowTitle('Players')

        self.pushButton.clicked.connect(self.player)
        self.pushButton_2.clicked.connect(self.clear)
        self.pushButton_3.clicked.connect(self.close)

    def player(self):
        # создаю try, чтобы избежать вылетов программы из-за неправильного ввода
        try:
            text = self.textEdit.toPlainText()
            # подсоединяю БД
            sqlite_connection = sqlite3.connect('Players')
            cursor = sqlite_connection.cursor()
            # ищу введённого игрока в БД
            cursor.execute(f'SELECT * FROM Players WHERE ФИО="{text}";')
            itog = cursor.fetchone()
            # присваиваю каждой ячейке свою переменную
            club = itog[1]
            country = itog[2]
            birthday_year = itog[3]
            position = itog[5]
            awards = itog[4]

            cursor.close()
            # вывожу в каждое поле вывода свою информацию
            self.textEdit_2.setText(club)
            self.textEdit_3.setText(country)
            self.textEdit_4.setText(birthday_year)
            self.textEdit_5.setText(position)
            self.textEdit_6.setText(awards)
        except TypeError:
            # задаю ошибку
            self.error_message()

    # задаю функцию ошибки
    def error_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle('Error')
        msg.setText(
            'Извините, мы не можем найти информацию о данном игроке. Проверьте правильность ввода и повторите попытку.')
        msg.exec_()

    # создаю функцию очистки поля ввода
    def clear(self):
        self.textEdit.clear()
        self.textEdit_2.clear()
        self.textEdit_3.clear()
        self.textEdit_4.clear()
        self.textEdit_5.clear()
        self.textEdit_6.clear()


if __name__ == "__main__":
    a = QtWidgets.QApplication(sys.argv)
    app = ADD()
    app.show()
    a.exec_()
