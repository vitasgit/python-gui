# window.py — главное окно приложения
# Отвечает за: отображение таблицы, строку поиска, кнопку добавления.
# НЕ знает SQL — для данных вызывает функции из db.py.
# НЕ знает как устроена форма добавления — для этого есть add_dialog.py.

from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QDialog
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import db
from add_dialog import AddDialog


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Программы')
        self.setGeometry(300, 100, 950, 650)

        main_layout = QVBoxLayout()

        # ── Верхняя панель: поиск и кнопка добавления ──────────────────────
        top_layout = QHBoxLayout()

        # Поле поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Поиск по ключевым словам...')
        self.search_input.setFixedHeight(35)

        # textChanged — сигнал: срабатывает каждый раз когда меняется текст.
        # Это удобнее чем кнопка "Найти": пользователь печатает — таблица обновляется.
        self.search_input.textChanged.connect(self.on_search_changed)

        # Кнопка сброса поиска
        btn_clear = QPushButton('✕')
        btn_clear.setFixedSize(35, 35)
        btn_clear.setToolTip('Сбросить поиск')
        btn_clear.clicked.connect(self.clear_search)

        # Кнопка добавления
        btn_add = QPushButton('+ Добавить')
        btn_add.setFixedHeight(35)
        btn_add.clicked.connect(self.open_add_dialog)

        top_layout.addWidget(self.search_input)
        top_layout.addWidget(btn_clear)
        top_layout.addWidget(btn_add)
        main_layout.addLayout(top_layout)

        # ── Метка с количеством результатов ────────────────────────────────
        self.count_label = QLabel()
        self.count_label.setStyleSheet('color: gray; font-size: 11px;')
        main_layout.addWidget(self.count_label)

        # ── Таблица ─────────────────────────────────────────────────────────
        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # нельзя редактировать
        self.table.verticalHeader().hide()                       # скрыть номера строк
        self.table.horizontalHeader().setStretchLastSection(True)# последний столбец растягивается

        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

        # Загружаем все данные при старте
        self.load_table(db.get_all_programs())

    # ── Методы ──────────────────────────────────────────────────────────────

    def load_table(self, data):
        """
        Заполняет таблицу данными.
        
        Принимает список словарей (результат из db.py).
        Не делает запросов к БД сам — только рисует то что получил.
        
        Почему вынесено отдельно от get_data?
        Потому что и поиск, и "показать все" рисуют таблицу одинаково —
        разница только в том КАКИЕ данные передать. Не дублируем код.
        """
        # Очищаем таблицу перед заполнением
        self.table.setRowCount(0)

        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Название', 'Описание', 'Год основания', 'Снимок'])
        self.table.setColumnWidth(0, 160)
        self.table.setColumnWidth(1, 260)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 220)

        for row, prog in enumerate(data):
            self.table.insertRow(row)

            # Название
            self.table.setItem(row, 0, QTableWidgetItem(prog['nazvanie'] or ''))

            # Описание
            self.table.setItem(row, 1, QTableWidgetItem(prog['opisanie'] or ''))

            # Год основания — это объект даты или строка, приводим к строке
            date_val = prog['god_osnovania']
            date_str = str(date_val) if date_val else '—'
            self.table.setItem(row, 2, QTableWidgetItem(date_str))

            # Картинка
            # Приоритет: сначала пробуем img_data (бинарные данные из БД),
            # если их нет — пробуем загрузить файл по имени
            pixmap = self._load_pixmap(prog['img_data'], prog['img'])

            if pixmap and not pixmap.isNull():
                pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                label = QLabel()
                label.setPixmap(pixmap)
                label.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(row, 3, label)
                self.table.setRowHeight(row, 160)
            else:
                # Картинки нет — показываем имя файла текстом
                self.table.setItem(row, 3, QTableWidgetItem(prog['img'] or '—'))
                self.table.setRowHeight(row, 30)

        # Обновляем счётчик результатов
        self.count_label.setText(f'Найдено записей: {len(data)}')

    def _load_pixmap(self, img_data, img_filename):
        """
        Вспомогательный метод: пытается получить QPixmap.
        Сначала из бинарных данных (img_data), потом из файла (img_filename).
        
        Подчёркивание в начале имени (_load_pixmap) — соглашение Python:
        "этот метод для внутреннего использования внутри класса".
        """
        pixmap = QPixmap()

        if img_data:
            # Загружаем из байт — PostgreSQL вернул bytea как bytes
            pixmap.loadFromData(bytes(img_data))
            if not pixmap.isNull():
                return pixmap

        if img_filename:
            # Запасной вариант — пробуем загрузить файл
            path = f"/home/student/Документы/Жданов/Приложение/imgs/{img_filename}"
            pixmap.load(path)

        return pixmap

    def on_search_changed(self, text):
        """
        Вызывается автоматически при каждом изменении текста в поле поиска.
        
        Если текст пустой — показываем все программы.
        Если есть текст — ищем по ключевым словам.
        """
        text = text.strip()
        if not text:
            # Поле очищено — показать всё
            self.load_table(db.get_all_programs())
        else:
            # Передаём текст в функцию поиска
            results = db.search_programs(text)
            self.load_table(results)

    def clear_search(self):
        """Очищает поле поиска. on_search_changed сработает автоматически."""
        self.search_input.clear()

    def open_add_dialog(self):
        """Открывает диалог добавления. После успеха — перезагружает таблицу."""
        dialog = AddDialog()
        if dialog.exec_() == QDialog.Accepted:
            # Если в поиске что-то введено — обновляем с учётом поиска
            # Если поле пустое — показываем всё
            self.on_search_changed(self.search_input.text())
