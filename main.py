from PyQt5.QtWidgets import QApplication
from GUI.MainWindow import MainWindow
import sys



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    #window.show()
    app.exec_()


if __name__ == '__main__':
    main()
