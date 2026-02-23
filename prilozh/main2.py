#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QDialog, QLineEdit, QFormLayout, QMessageBox, QDateEdit
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QDate


# ======================================================
# ДИАЛОГОВОЕ ОКНО ДЛЯ ДОБАВЛЕНИЯ НОВОЙ ЗАПИСИ
# QDialog — это специальный виджет для диалогов.
# Он открывается поверх главного окна и "блокирует" его
# (это называется модальный режим — exec_())
# ======================================================
class AddDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить программу')
        self.setFixedSize(400, 280)

        # QFormLayout — удобный макет для форм: слева метка, справа поле ввода
        layout = QFormLayout()

        # Поля ввода — QLineEdit это однострочное текстовое поле
        self.input_name = QLineEdit()
        self.input_desc = QLineEdit()
        self.input_img  = QLineEdit()
        self.input_img.setPlaceholderText('например: gimp.png')  # подсказка внутри поля

        # QDateEdit — специальный виджет для выбора даты
        self.input_date = QDateEdit()
        self.input_date.setCalendarPopup(True)       # кнопка-календарик для выбора
        self.input_date.setDate(QDate.currentDate()) # по умолчанию — сегодня

        # Добавляем поля в форму: ('Метка', виджет)
        layout.addRow('Название:', self.input_name)
        layout.addRow('Описание:', self.input_desc)
        layout.addRow('Год основания:', self.input_date)
        layout.addRow('Имя файла картинки:', self.input_img)

        # Кнопки: Сохранить и Отмена
        btn_save   = QPushButton('Сохранить')
        btn_cancel = QPushButton('Отмена')

        # Привязываем кнопки к методам
        btn_save.clicked.connect(self.save)     # нажали Сохранить -> вызвать self.save
        btn_cancel.clicked.connect(self.reject) # reject() — стандартный метод QDialog: закрыть с результатом "отклонено"

        # Кнопки кладём рядом в горизонтальный контейнер
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)

        layout.addRow(btn_layout)
        self.setLayout(layout)

    def save(self):
        # Считываем введённые данные
        name = self.input_name.text().strip()  # .strip() убирает пробелы по краям
        desc = self.input_desc.text().strip()
        img  = self.input_img.text().strip()
        date = self.input_date.date().toString('yyyy-MM-dd')  # формат для PostgreSQL

        # Проверяем что поле "Название" не пустое — минимальная валидация
        if not name:
            # QMessageBox.warning — всплывающее предупреждение
            QMessageBox.warning(self, 'Ошибка', 'Поле "Название" обязательно!')
            return  # выходим из метода, не закрывая диалог

        # Выполняем SQL-запрос INSERT
        # Используем :name, :desc и т.д. вместо прямой подстановки строк —
        # это называется параметризованный запрос (защита от SQL-инъекций)
        q = QSqlQuery()
        q.prepare('''
            INSERT INTO prog (nazvanie, opisanie, god_osnovania, img)
            VALUES (:name, :desc, :date, :img)
        ''')
        # Привязываем реальные значения к заполнителям
        q.bindValue(':name', name)
        q.bindValue(':desc', desc)
        q.bindValue(':date', date)
        q.bindValue(':img',  img)

        # Выполняем запрос. exec_() возвращает True если успешно
        if q.exec_():
            self.accept()  # accept() — стандартный метод QDialog: закрыть с результатом "принято"
        else:
            # Если ошибка — показываем текст ошибки от PostgreSQL
            QMessageBox.critical(self, 'Ошибка БД', q.lastError().text())


# ======================================================
# ГЛАВНОЕ ОКНО
# ======================================================
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Программы')
        self.setGeometry(300, 100, 900, 600)

        # QVBoxLayout — вертикальный контейнер: элементы идут сверху вниз
        main_layout = QVBoxLayout()

        # --- Кнопка "Добавить" ---
        btn_add = QPushButton('+ Добавить программу')
        btn_add.setFixedHeight(35)
        btn_add.clicked.connect(self.open_add_dialog)  # нажатие -> открыть диалог
        main_layout.addWidget(btn_add)

        # --- Таблица ---
        self.table = QTableWidget()

        # Запрет редактирования ячеек напрямую
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Скрыть нумерацию строк слева
        self.table.verticalHeader().hide()

        # Растягивать последний столбец до края окна
        self.table.horizontalHeader().setStretchLastSection(True)

        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

        # Загружаем данные при старте
        self.get_data()

    def get_data(self):
        # Сначала очищаем таблицу (на случай перезагрузки после добавления)
        self.table.setRowCount(0)

        # SQL-запрос: берём все поля кроме id
        q = QSqlQuery()
        q.exec_('SELECT nazvanie, opisanie, god_osnovania, img FROM prog ORDER BY id')

        # 4 столбца
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Название', 'Описание', 'Год основания', 'Снимок'])

        # Задаём ширину столбцов вручную
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 250)

        row = 0
        while q.next():
            self.table.insertRow(row)

            # Столбец 0: Название
            self.table.setItem(row, 0, QTableWidgetItem(q.value(0)))

            # Столбец 1: Описание
            self.table.setItem(row, 1, QTableWidgetItem(q.value(1)))

            # Столбец 2: Год основания
            # q.value(2) возвращает объект QDate, переводим в строку
            date_val = q.value(2)
            if date_val:
                date_str = str(date_val)  # будет вида '1997-05-26'
            else:
                date_str = '—'
            self.table.setItem(row, 2, QTableWidgetItem(date_str))

            # Столбец 3: Картинка
            img_name = q.value(3)
            full_path = f"/home/student/Документы/Жданов/Приложение/imgs/{img_name}"
            pixmap = QPixmap(full_path)

            if not pixmap.isNull():  # проверяем что файл найден и загрузился
                pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio)  # сохраняем пропорции
                label = QLabel()
                label.setPixmap(pixmap)
                label.setAlignment(Qt.AlignCenter)  # по центру ячейки
                self.table.setCellWidget(row, 3, label)
                self.table.setRowHeight(row, 160)
            else:
                # Если файл не найден — просто пишем имя файла текстом
                self.table.setItem(row, 3, QTableWidgetItem(img_name or '—'))
                self.table.setRowHeight(row, 30)

            row += 1

    def open_add_dialog(self):
        # Создаём экземпляр нашего диалога
        dialog = AddDialog()

        # exec_() открывает диалог в МОДАЛЬНОМ режиме —
        # пользователь не может кликать на главное окно пока диалог открыт.
        # exec_() возвращает QDialog.Accepted (1) если нажали Сохранить
        # и QDialog.Rejected (0) если нажали Отмена или закрыли крестиком
        if dialog.exec_() == QDialog.Accepted:
            # Запись успешно добавлена — перезагружаем таблицу
            self.get_data()


# ======================================================
# ПОДКЛЮЧЕНИЕ К БД — делается ДО создания окна
# ======================================================
db = QSqlDatabase.addDatabase('QPSQL')
db.setHostName('localhost')
db.setDatabaseName('programms')
db.setPort(5432)
db.setUserName('postgres')
db.setPassword('123456')

if not db.open():
    print('Ошибка подключения к БД:', db.lastError().text())
    sys.exit(1)  # завершаем программу если нет подключения

app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec())
