import cv2
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QDialog, QMessageBox, QPushButton

from GUI.UserWindow import UserWindow
from facerecognition.facerecognizer import FaceRecognizer


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
            if(self.isFree):
                self.login.emit("xd")
                self.isFree = False


class MainWindow(QMainWindow):

    def __init__(self,parent = None):
        super().__init__()
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

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(str)
    def loginUser(self, user):
        self.Loginmsg.setText("Hi {}!\n Would you like to log in? ".format(user))
        self.Loginmsg.show()

    @pyqtSlot()
    def UserWindow(self):
        self.video.isFree = True


    def loginButton_clicked(self, i):
        if i.text() == "OK":
            self.Loginmsg.close()
            self.OpenUserWindow()
        else:
            self.video.isFree = True

    def OpenUserWindow(self):
        self.User = UserWindow()
        self.User.closeInfo.connect(self.UserWindow)
        self.User.show()




def keyPressEvent(self, e):
        if e.key() == Qt.Key_F9:
            self.close()
