from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QTextBrowser
from PyQt5.QtCore import pyqtSignal, QRect, QMetaObject, QCoreApplication


class UserWindow(QWidget):
    close = pyqtSignal()

    def setupUi(self, Form):
        self.Form = Form
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.pushButton = QPushButton(Form)
        self.pushButton.setGeometry(QRect(250, 30, 121, 61))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setGeometry(QRect(250, 110, 121, 61))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QPushButton(Form)
        self.pushButton_3.clicked.connect(self.DzialajPls)
        self.pushButton_3.setGeometry(QRect(250, 200, 121, 61))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label = QLabel(Form)
        self.label.setGeometry(QRect(20, 10, 200, 31))
        self.label.setObjectName("label")
        self.textBrowser = QTextBrowser(Form)
        self.textBrowser.setGeometry(QRect(10, 60, 181, 192))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "NEXT"))
        self.pushButton_2.setText(_translate("Form", "WRITE"))
        self.pushButton_3.setText(_translate("Form", "LOG OUT"))
        self.label.setText(_translate("Form", "Masz {} nowych wiadomosci".format(0)))

    def DzialajPls(self):
        self.close.emit()
        self.Form.close()

