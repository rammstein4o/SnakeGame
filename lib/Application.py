from PyQt5.QtWidgets import QApplication
from lib.UserInterface import UserInterface

class Application(QApplication):

    def __init__(self, config):
        super(Application, self).__init__([])
        self.config = config

    def run(self):
        ui = UserInterface(self.config)
        ui.createWindow()
        self.exec_()
