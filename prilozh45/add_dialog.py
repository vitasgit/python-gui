from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QHBoxLayout, QVBoxLayout,
    QLineEdit, QPushButton, QLabel,
    QFileDialog, QCheckBox, QScrollArea, QWidget, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import db 


class AddDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить программу')
        self.setFixedSize(460, 520)

        self.img_bytes    = None
        self.img_filename = ''

        # Основной вертикальный макет
        main_layout = QVBoxLayout()

        form = QFormLayout()

        self.input_name = QLineEdit()
        self.input_desc = QLineEdit()

        form.addRow('Название:', self.input_name)
        form.addRow('Описание:', self.input_desc)

        main_layout.addLayout(form)

        # --- Выбор картинки ---
        img_layout = QHBoxLayout()

        btn_img = QPushButton('Выбрать картинку...')
        btn_img.clicked.connect(self.choose_image)

        self.img_preview = QLabel('Картинка не выбрана')
        self.img_preview.setFixedSize(100, 80)
        self.img_preview.setAlignment(Qt.AlignCenter)
        self.img_preview.setStyleSheet('border: 1px solid gray;')

        img_layout.addWidget(btn_img)
        img_layout.addWidget(self.img_preview)
        main_layout.addLayout(img_layout)

        # --- Ключевые слова ---
        main_layout.addWidget(QLabel('Ключевые слова:'))

        scroll = QScrollArea()
        scroll.setFixedHeight(150)
        scroll.setWidgetResizable(True)

        # Контейнер внутри scroll
        kw_container = QWidget()
        kw_layout    = QVBoxLayout()
        kw_container.setLayout(kw_layout)

        self.checkboxes = []

        keywords = db.get_all_keywords()
        if keywords:
            for kw_id, kw_name in keywords:
                cb = QCheckBox(kw_name)
                kw_layout.addWidget(cb)
                self.checkboxes.append((cb, kw_id))
        else:
            kw_layout.addWidget(QLabel('Нет ключевых слов в БД'))

        scroll.setWidget(kw_container)
        main_layout.addWidget(scroll)

        # --- Поле для нового ключевого слова ---
        new_kw_layout = QHBoxLayout()
        self.input_new_keyword = QLineEdit()
        self.input_new_keyword.setPlaceholderText('Новое ключевое слово...')
        btn_add_kw = QPushButton('Добавить')
        btn_add_kw.clicked.connect(self.add_new_keyword)
        new_kw_layout.addWidget(self.input_new_keyword)
        new_kw_layout.addWidget(btn_add_kw)
        main_layout.addLayout(new_kw_layout)

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

    def add_new_keyword(self):
        """Добавляет новое ключевое слово в БД и добавляет чекбокс в список"""
        kw_name = self.input_new_keyword.text().strip()
        
        if not kw_name:
            QMessageBox.warning(self, 'Ошибка', 'Введите название ключевого слова')
            return
        
        # Добавляем ключевое слово в БД
        new_kw_id = db.add_keyword(kw_name)
        
        if new_kw_id is None:
            QMessageBox.warning(self, 'Ошибка', 'Не удалось добавить ключевое слово')
            return
        
        # Добавляем чекбокс с новым ключевым словом в список
        cb = QCheckBox(kw_name)
        cb.setChecked(True)  # Сразу отмечаем новое ключевое слово
        self.input_new_keyword.clear()
        
        # Находим контейнер с чекбоксами и добавляем туда новый
        scroll = self.findChild(QScrollArea)
        if scroll:
            container = scroll.widget()
            layout = container.layout()
            layout.addWidget(cb)
            self.checkboxes.append((cb, new_kw_id))

    def choose_image(self):
        # QFileDialog.getOpenFileName возвращает (путь, фильтр)
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Выберите картинку',
            '',                          
            'Изображения (*.png *.jpg *.jpeg *.bmp)'
        )

        if not path:
            return 


        with open(path, 'rb') as f:
            self.img_bytes = f.read()

        self.img_filename = path.split('/')[-1]

        pixmap = QPixmap()
        pixmap.loadFromData(self.img_bytes)
        pixmap = pixmap.scaled(100, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.img_preview.setPixmap(pixmap)
        self.img_preview.setText('')

    def save(self):
        name = self.input_name.text().strip()
        desc = self.input_desc.text().strip()

        if not name:
            QMessageBox.warning(self, 'Ошибка')
            return

        selected_kw_ids = [kw_id for cb, kw_id in self.checkboxes if cb.isChecked()]

        success = db.add_program(
            nazvanie      = name,
            opisanie      = desc,
            god_osnovania = None,
            img_filename  = self.img_filename,
            img_bytes     = self.img_bytes,
            keyword_ids   = selected_kw_ids
        )

        if success:
            self.accept()
