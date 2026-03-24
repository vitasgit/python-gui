from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QCheckBox, QScrollArea, QWidget,
    QPushButton, QLabel
)
import db


class FilterDialog(QDialog):
    def __init__(self, previously_selected=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Фильтр по ключевым словам')
        self.setFixedSize(360, 420)

        if previously_selected is None:
            previously_selected = []

        self.selected_ids = []
        self.checkboxes   = []

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Выберите ключевые слова:'))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container    = QWidget()
        cb_layout    = QVBoxLayout()
        container.setLayout(cb_layout)

        keywords = db.get_all_keywords()

        if keywords:
            for kw_id, kw_name in keywords:
                cb = QCheckBox(kw_name)
                if kw_id in previously_selected:
                    cb.setChecked(True)
                cb_layout.addWidget(cb)
                self.checkboxes.append((cb, kw_id))
        else:
            cb_layout.addWidget(QLabel('Нет ключевых слов в БД'))

        scroll.setWidget(container)
        layout.addWidget(scroll)

        # --- Кнопки ---
        btn_layout = QHBoxLayout()

        btn_apply = QPushButton('Применить')
        btn_apply.clicked.connect(self._apply)

        btn_reset = QPushButton('Сбросить')
        btn_reset.clicked.connect(self._reset)

        btn_cancel = QPushButton('Отмена')
        btn_cancel.clicked.connect(self.reject)

        btn_layout.addWidget(btn_apply)
        btn_layout.addWidget(btn_reset)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def _apply(self):
        self.selected_ids = [kw_id for cb, kw_id in self.checkboxes if cb.isChecked()]
        self.accept()

    def _reset(self):
        for cb, _ in self.checkboxes:
            cb.setChecked(False)
        self.selected_ids = []
        self.accept()