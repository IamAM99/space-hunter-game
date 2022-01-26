import sys
from PySide2 import QtCore
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QMainWindow, QGraphicsDropShadowEffect, QApplication
from src.loading_setup import Ui_SplashScreen
from src.game_loop import open_game_window


class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        # Counter
        self.counter = 0

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
        self.timer.start(40)

        # CHANGE DESCRIPTION

        # Initial Text
        QtCore.QTimer.singleShot(
            2500,
            lambda: self.ui.label_description.setText(
                "<strong>WELCOME</strong> TO OUR GAME"
            ),
        )

        # Change Texts
        QtCore.QTimer.singleShot(
            3500,
            lambda: self.ui.label_description.setText(
                "<strong>LOADING</strong> THE STARSHIP"
            ),
        )
        QtCore.QTimer.singleShot(
            5000,
            lambda: self.ui.label_description.setText(
                "<strong>SPAWNING</strong> ENEMIES"
            ),
        )
        self.show()

    def progress(self):

        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(self.counter)

        # CLOSE SPLASH SCREE AND OPEN APP
        if self.counter > 100:
            # STOP TIMER
            self.timer.stop()
            # CLOSE SPLASH SCREEN
            self.close()
            open_game_window()
        self.counter += 1


def start_game():
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start_game()
