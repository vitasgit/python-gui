#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import QApplication
from window import Window
from db_login_dialog import DBLoginDialog


def main():
    app = QApplication(sys.argv)

    # Сначала показываем окно авторизации к БД
    db_dialog = DBLoginDialog()
    if db_dialog.exec_() != 1:
        # Пользователь нажал "Отмена" — выходим
        sys.exit(0)

    # Если подключение прошло успешно — запускаем главное окно
    win = Window()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
