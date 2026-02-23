#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,  QLabel
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QPixmap, QIcon


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Программы')
        self.setGeometry(300, 300, 600, 400)

        # Создаём таблицу
        self.table = QTableWidget(self)
        self.table.setGeometry(10, 10, 580, 380)

        # Запрет редактирования
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Скрыть нумерацию строк слева
        self.table.verticalHeader().hide()

        # Заполняем таблицу данными
        self.get_data()

    def get_data(self):
        # Делаем запрос
        q = QSqlQuery()
        q.exec_('select nazvanie, opisanie, img from prog')

        # Устанавливаем заголовки столбцов
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Название', 'Описание', 'Снимок'])

        # Перебираем строки результата
        row = 0
        while q.next():
            self.table.insertRow(row)  # добавить строку
            # Записываем каждую ячейку
            self.table.setItem(row, 0, QTableWidgetItem(q.value(0)))
            self.table.setItem(row, 1, QTableWidgetItem(q.value(1)))

            img_name = q.value(2)
            full_path = f"/home/student/Документы/Жданов/Приложение/imgs/{img_name}"
            pixmap = QPixmap(full_path)
            pixmap = pixmap.scaled(300, 300)

            # Создаём label и вставляем в ячейку
            label = QLabel()
            label.setPixmap(pixmap)

            self.table.setRowHeight(row, 200)       # высота строки под картинку
            self.table.setColumnWidth(2, 300)        # ширина столбца под картинку
            self.table.setCellWidget(row, 2, label)  # вставляем label вместо item

            row += 1


# Подключение к БД
db = QSqlDatabase.addDatabase('QPSQL')
db.setHostName('localhost')
db.setDatabaseName('programms')
db.setPort(5432)
db.setUserName('postgres')
db.setPassword('123456')

if not db.open():
    print('Ошибка подключения')


app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec())