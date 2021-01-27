import cv2
import sys
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QDialog, QMessageBox, QPushButton, QGridLayout
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap


class UserWindow(QWidget):
    closeInfo = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.resize(620, 620)
        layout = QGridLayout()

        self.label = QLabel("xd")
        layout.addWidget(self.label)

        self.button = QPushButton('Close')
        self.button.clicked.connect(self.closeUserWindow)

        layout.addWidget(self.button)

        self.setLayout(layout)

    def closeUserWindow(self ) :
        self.close.emit()
        self.close()
