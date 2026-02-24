# add_dialog.py — диалог добавления новой программы
# Этот файл знает КАК выглядит форма добавления.
# Он не знает ничего про таблицу в главном окне — это не его дело.
# Когда пользователь нажимает "Сохранить", диалог вызывает функцию из db.py
# и закрывается. Главное окно само решит что делать дальше (перезагрузить таблицу).

from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QHBoxLayout, QVBoxLayout,
    QLineEdit, QDateEdit, QPushButton, QLabel,
    QFileDialog, QCheckBox, QScrollArea, QWidget, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QDate
import db  # наш слой данных


class AddDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить программу')
        self.setFixedSize(460, 520)

        # Здесь будем хранить байты выбранной картинки (или None)
        self.img_bytes    = None
        self.img_filename = ''

        # Основной вертикальный макет
        main_layout = QVBoxLayout()

        # --- Форма с полями ввода ---
        form = QFormLayout()

        self.input_name = QLineEdit()
        self.input_desc = QLineEdit()

        self.input_date = QDateEdit()
        self.input_date.setCalendarPopup(True)
        self.input_date.setDate(QDate.currentDate())

        form.addRow('Название:',      self.input_name)
        form.addRow('Описание:',      self.input_desc)
        form.addRow('Год основания:', self.input_date)

        main_layout.addLayout(form)

        # --- Выбор картинки ---
        img_layout = QHBoxLayout()

        # Кнопка открытия файлового диалога
        btn_img = QPushButton('Выбрать картинку...')
        btn_img.clicked.connect(self.choose_image)

        # Метка для предпросмотра
        self.img_preview = QLabel('Картинка не выбрана')
        self.img_preview.setFixedSize(100, 80)
        self.img_preview.setAlignment(Qt.AlignCenter)
        self.img_preview.setStyleSheet('border: 1px solid gray;')

        img_layout.addWidget(btn_img)
        img_layout.addWidget(self.img_preview)
        main_layout.addLayout(img_layout)

        # --- Ключевые слова ---
        # Загружаем все слова из БД и показываем как чекбоксы
        main_layout.addWidget(QLabel('Ключевые слова:'))

        # QScrollArea — прокручиваемая область (если слов будет много)
        scroll = QScrollArea()
        scroll.setFixedHeight(150)
        scroll.setWidgetResizable(True)

        # Контейнер внутри scroll
        kw_container = QWidget()
        kw_layout    = QVBoxLayout()
        kw_container.setLayout(kw_layout)

        # self.checkboxes — список (checkbox_виджет, id_слова)
        # Нам нужно потом знать id выбранных слов
        self.checkboxes = []

        keywords = db.get_all_keywords()  # [(id, nazvanie), ...]
        if keywords:
            for kw_id, kw_name in keywords:
                cb = QCheckBox(kw_name)
                kw_layout.addWidget(cb)
                self.checkboxes.append((cb, kw_id))
        else:
            kw_layout.addWidget(QLabel('Нет ключевых слов в БД'))

        scroll.setWidget(kw_container)
        main_layout.addWidget(scroll)

        # --- Кнопки ---
        btn_layout = QHBoxLayout()
        btn_save   = QPushButton('Сохранить')
        btn_cancel = QPushButton('Отмена')
        btn_save.clicked.connect(self.save)
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    def choose_image(self):
        """
        Открывает файловый диалог для выбора картинки.
        Читает файл в байты и показывает предпросмотр.
        """
        # QFileDialog.getOpenFileName возвращает (путь, фильтр)
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Выберите картинку',
            '',                          # начальная папка (пустая = домашняя)
            'Изображения (*.png *.jpg *.jpeg *.bmp)'  # фильтр файлов
        )

        if not path:
            return  # пользователь нажал Отмена в диалоге

        # Читаем файл как байты — это и будет храниться в PostgreSQL (bytea)
        with open(path, 'rb') as f:  # 'rb' = read binary (читать бинарно)
            self.img_bytes = f.read()

        # Сохраняем только имя файла (без пути), на случай если понадобится
        self.img_filename = path.split('/')[-1]

        # Показываем предпросмотр — QPixmap умеет загружаться из байт через fromData
        pixmap = QPixmap()
        pixmap.loadFromData(self.img_bytes)
        pixmap = pixmap.scaled(100, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.img_preview.setPixmap(pixmap)
        self.img_preview.setText('')  # убираем текст "Картинка не выбрана"

    def save(self):
        """
        Собирает данные из формы и вызывает db.add_program().
        """
        name = self.input_name.text().strip()
        desc = self.input_desc.text().strip()
        date = self.input_date.date().toString('yyyy-MM-dd')

        if not name:
            QMessageBox.warning(self, 'Ошибка', 'Поле "Название" обязательно!')
            return

        # Собираем id выбранных ключевых слов
        # Проходим по списку чекбоксов и берём id тех, что отмечены
        selected_kw_ids = [kw_id for cb, kw_id in self.checkboxes if cb.isChecked()]

        # Вызываем функцию из db.py — диалог не пишет SQL сам
        success = db.add_program(
            nazvanie      = name,
            opisanie      = desc,
            god_osnovania = date,
            img_filename  = self.img_filename,
            img_bytes     = self.img_bytes,
            keyword_ids   = selected_kw_ids
        )

        if success:
            self.accept()  # закрываем диалог с результатом "успех"
