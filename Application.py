from PyQt5.QtWidgets import QApplication, QWidget

class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)