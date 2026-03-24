#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtSql import QSqlDatabase
from window import Window


def connect_db():
    db = QSqlDatabase.addDatabase('QPSQL')
    db.setHostName('localhost')
    db.setDatabaseName('programms')
    db.setPort(5432)
    db.setUserName('postgres')
    db.setPassword('123456')

    if not db.open():
        return False

    return True


def main():
    app = QApplication(sys.argv)

    if not connect_db():
        print("Ошибка подключения БД")
        sys.exit(1)

    win = Window()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
