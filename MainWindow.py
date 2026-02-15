from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot
from MainMenu import MainMenu

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # создаем объект, родитель - главное окно
        # self - главное окно
        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)

        # Подключаем сигнал triggered пункта "About" к слоту
        main_menu.about.triggered.connect(self.about)

    @pyqtSlot() # декоратор слота
    def about(self):
        title = "БД программ"
        text = "Хранит список программ, информацию о программе, ссылки для скачивания т.д."
        QMessageBox.about(self, title, text)


