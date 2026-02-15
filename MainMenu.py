from PyQt5.QtWidgets import QMenuBar

class MainMenu(QMenuBar):
    def __init__(self, parent = None):
        super().__init__(parent)

        help_menu = self.addMenu('Справка')
        self.about = help_menu.addAction('О программе...')