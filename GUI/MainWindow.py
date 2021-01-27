import cv2
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QDialog, QMessageBox, QWidget

from GUI.UserWindow import UserWindow
from facerecognition.facerecognizer import FaceRecognizer
import random


class VideoThread(QThread):
    changePixmap = pyqtSignal(QImage)
    login = pyqtSignal(str)
    def run(self):
        self.isFree = True
        fr = FaceRecognizer()
        while True:
            fr._update()
            frame = fr.get_frame(mark_faces=True)
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(1600, 1200, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)
            person = fr.get_recognized_face()
            if(self.isFree and  person != None):
                self.login.emit(person)
                self.isFree = False




class MainWindow(QMainWindow):

    def __init__(self,parent = None):
        super().__init__()
        self.currentUser = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle("SW")
        self.disply_width = 1600
        self.display_height = 1200
        self.resize(self.disply_width,self.display_height)

        self.Loginmsg = QMessageBox()
        self.Loginmsg.setWindowFlag(Qt.FramelessWindowHint)
        self.Loginmsg.setStandardButtons(QMessageBox.Ok | QMessageBox.No)
        self.Loginmsg.buttonClicked.connect(self.loginButton_clicked)
        self.Loginmsg.setEscapeButton(QMessageBox.No)


        self.label = QLabel(self)
        self.label.resize( self.disply_width, self.display_height)
        self.video = VideoThread(self)
        self.video.changePixmap.connect(self.setImage)
        self.video.login.connect(self.loginUser)
        self.video.start()

        self.show()

    def openSecond(self):
        myDialof = QDialog(self)
        myDialof.show()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(str)
    def loginUser(self, user):
        self.currentUser = user
        self.Loginmsg.setText("Hi {}!\n Would you like to log in? ".format(self.currentUser))
        self.Loginmsg.show()

    @pyqtSlot()
    def UserWindowClose(self):
        self.video.isFree = True


    def loginButton_clicked(self, i):
        if i.text() == "OK":
            self.Loginmsg.close()
            self.OpenUserWindow()
        else:
            self.video.isFree = True

    def LoginClose(self):
        self.video.isFree = True
        self.close()


    def OpenUserWindow(self):

        self.Form = QWidget()
        self.ui = UserWindow()
        self.ui.close.connect(self.UserWindowClose)
        self.ui.setupUi(self.Form)
        self.Form.show()



    def keyPressEvent(self, e):
            if e.key() == Qt.Key_F9:
                self.close()
