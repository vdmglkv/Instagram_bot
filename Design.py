from PyQt5 import uic, QtWidgets
import sys
from Bot import InstagramBot
from aut_date import username, password

Form, _ = uic.loadUiType("mainapp.ui")


class MainApp(QtWidgets.QMainWindow, Form):

    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.print_button_pressed)

    @staticmethod
    def print_button_pressed(self):
        bot = InstagramBot(username, password)
        bot.login()


try:
    app = QtWidgets.QApplication([])
    window = MainApp()
    window.show()

except Exception as ex:
    print(ex)

sys.exit(app.exec_())
