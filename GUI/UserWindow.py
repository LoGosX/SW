from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QTextBrowser, QTextEdit, QLineEdit
from PyQt5.QtCore import pyqtSignal, QRect, QMetaObject, QCoreApplication


class UserWindow(QWidget):
    close = pyqtSignal()

    def prepareData(self, name):
        self.user = name
        self.messages = []
        with open("GUI/messages.txt", "r") as f:
            lines = f.readlines()
            print(lines)
        with open("GUI/messages.txt", "w") as f:
            for line in lines:
                words = line.split(' ')
                print(words)
                print(' '.join(words[0:2]))
                if ' '.join(words[0:2]) != name:
                    f.write(line)
                else:
                    self.messages.append(line)

    def setupUi(self, Form):
        self.Form = Form
        Form.setObjectName("Face")
        Form.resize(400, 300)
        self.pushButton = QPushButton(Form)
        self.pushButton.clicked.connect(self.Next)
        self.pushButton.setGeometry(QRect(250, 30, 121, 61))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.clicked.connect(self.New)
        self.pushButton_2.setGeometry(QRect(250, 110, 121, 61))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QPushButton(Form)
        self.pushButton_3.clicked.connect(self.Quit)
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
        Form.setWindowTitle(_translate("Form", "FaceMessenger"))
        self.pushButton.setText(_translate("Form", "NEXT"))
        self.pushButton_2.setText(_translate("Form", "WRITE"))
        self.pushButton_3.setText(_translate("Form", "LOG OUT"))
        self.label.setText(_translate("Form", "Masz {} nowych wiadomosci".format(len(self.messages))))

    def Quit(self):
        self.user = ""
        self.messages = []
        self.close.emit()
        self.Form.close()

    def Next(self):
        self.textBrowser.clear()
        if len(self.messages) > 0:
            message = self.messages[0].split(' ')
            if (len(message) > 4):
                self.textBrowser.append("Wysylajacy: {} \n Wiadomosc: \n".format(message[2] + " " + message[3]))
                self.textBrowser.append(' '.join(message[4:]))
            self.messages = self.messages[1:]
            self.label.setText(
                QCoreApplication.translate("Form", "Masz {} nowych wiadomosci".format(len(self.messages))))

    def New(self):
        self.FormNew = QWidget()
        self.NewForm(self.FormNew)
        self.FormNew.show()

    def NewForm(self, Form):
        Form.setObjectName("Form")
        Form.resize(485, 142)
        self.label = QLabel(Form)
        self.label.setGeometry(QRect(10, 10, 91, 31))
        self.label.setObjectName("label")
        self.label_2 = QLabel(Form)
        self.label_2.setGeometry(QRect(10, 50, 47, 14))
        self.label_2.setObjectName("label_2")
        self.label_3 = QLabel(Form)
        self.label_3.setGeometry(QRect(10, 90, 47, 14))
        self.label_3.setObjectName("label_3")
        self.textEdit = QTextEdit(Form)
        self.textEdit.setGeometry(QRect(220, 10, 181, 121))
        self.textEdit.setObjectName("textEdit")
        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setGeometry(QRect(70, 50, 101, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QLineEdit(Form)
        self.lineEdit_2.setGeometry(QRect(70, 90, 101, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QPushButton(Form)
        self.pushButton.clicked.connect(self.Save)
        self.pushButton.setGeometry(QRect(420, 40, 51, 61))
        self.pushButton.setObjectName("pushButton")

        self.retranslateNew(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateNew(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Receiver:"))
        self.label_2.setText(_translate("Form", "Name"))
        self.label_3.setText(_translate("Form", "Surname"))
        self.pushButton.setText(_translate("Form", "Send"))

    def Save(self):
        with open("GUI/messages.txt", "a") as f:
            name = self.lineEdit.text()
            surname = self.lineEdit_2.text()
            data = self.textEdit.toPlainText()
            line = ' '.join([name, surname, self.user, data]) + '\n'
            f.write(line)
        self.FormNew.close()
