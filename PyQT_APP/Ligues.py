# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ligues.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(496, 300)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(120, 7, 96, 81))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(13)
        font.setItalic(False)
        font.setUnderline(False)
        font.setKerning(True)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(366, 100, 121, 71))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(13)
        font.setItalic(False)
        font.setUnderline(False)
        font.setKerning(True)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(370, 7, 111, 81))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(13)
        font.setItalic(False)
        font.setUnderline(False)
        font.setKerning(True)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(369, 177, 111, 81))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(13)
        font.setItalic(False)
        font.setUnderline(False)
        font.setKerning(True)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(80, 107, 141, 71))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(13)
        font.setItalic(False)
        font.setUnderline(False)
        font.setKerning(True)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_8 = QtWidgets.QPushButton(Form)
        self.pushButton_8.setGeometry(QtCore.QRect(70, 190, 151, 61))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(13)
        font.setItalic(False)
        font.setUnderline(False)
        font.setKerning(True)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(Form)
        self.pushButton_9.setGeometry(QtCore.QRect(20, 270, 89, 25))
        self.pushButton_9.setObjectName("pushButton_9")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(280, 100, 81, 71))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("La Liga.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(280, 10, 81, 81))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("Bundesliga.jpg"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(290, 180, 67, 81))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("Serie a.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(0, 196, 67, 51))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("Russian_Premier_League_Logo.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(10, 16, 101, 71))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("png-transparent-2017-18-premier-league-2016-17-premier-league-2018-19-premier-league-2015-16-premier-league-west-bromwich-albion-f-c-football-fan-purple-violet-text.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(0, 106, 71, 71))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("Ligue1.jpg"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Premier Ligue"))
        self.pushButton_2.setText(_translate("Form", "LaLiga Santander"))
        self.pushButton_3.setText(_translate("Form", "Bundesliga"))
        self.pushButton_4.setText(_translate("Form", "Serie A TIM"))
        self.pushButton_6.setText(_translate("Form", "Ligue 1 Uber Eats"))
        self.pushButton_8.setText(_translate("Form", "Russian Premier Ligue"))
        self.pushButton_9.setText(_translate("Form", "<- Назад"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
