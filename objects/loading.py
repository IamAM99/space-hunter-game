import sys
from PySide2 import QtCore
from PySide2.QtGui import QColor
from PySide2.QtWidgets import *

# ==> SPLASH SCREEN
from objects.loading_setup import Ui_SplashScreen

# ==> GLOBALS
counter = 0


class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        # REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        # QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(50)

        # CHANGE DESCRIPTION

        # Initial Text
        self.ui.label_description.setText("<strong>WELCOME</strong> TO OUR GAME")

        # Change Texts
        QtCore.QTimer.singleShot(
            1500,
            lambda: self.ui.label_description.setText(
                "<strong>LOADING</strong> DATABASE"
            ),
        )
        QtCore.QTimer.singleShot(
            3000,
            lambda: self.ui.label_description.setText(
                "<strong>LOADING</strong> USER INTERFACE"
            ),
        )
        self.show()

    def progress(self):

        global counter
        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(counter)

        # CLOSE SPLASH SCREE AND OPEN APP
        if counter > 100:
            # STOP TIMER
            self.timer.stop()
            # CLOSE SPLASH SCREEN
            self.close()
        counter += 1


def run_loading():
    app = QApplication(sys.argv)
    window = SplashScreen()
    # sys.exit(app.exec_())
    return app


if __name__ == "__main__":
    run_loading()
