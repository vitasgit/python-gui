from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QDialog
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import db
from add_dialog    import AddDialog
from filter_dialog import FilterDialog
from register_dialog import RegisterDialog
from login_dialog import LoginDialog


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Программы')
        self.setGeometry(300, 100, 950, 650)

        self.active_keyword_ids = []
        self.current_user = None  # Текущий авторизованный пользователь
        self.show_favorites_only = False  # Показывать только избранное

        main_layout = QVBoxLayout()
        top_layout  = QHBoxLayout()

        # ── Поиск по названию ──
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Поиск по названию...')
        self.search_input.setFixedHeight(35)
        self.search_input.textChanged.connect(self.apply_filters)

        btn_clear = QPushButton('✕')
        btn_clear.setFixedSize(35, 35)
        btn_clear.clicked.connect(self.clear_search)

        # ── Кнопка фильтра ──
        self.btn_filter = QPushButton('Фильтр')
        self.btn_filter.setFixedHeight(35)
        self.btn_filter.clicked.connect(self.open_filter_dialog)

        # ── Кнопка фильтра избранного ──
        self.btn_favorites = QPushButton('☆ Избранное')
        self.btn_favorites.setFixedHeight(35)
        self.btn_favorites.clicked.connect(self.toggle_favorites_filter)
        self.btn_favorites.setEnabled(False)  # Неактивна, пока пользователь не авторизован

        # ── Кнопка добавления ── (только для admin)
        self.btn_add = QPushButton('Добавить')
        self.btn_add.setFixedHeight(35)
        self.btn_add.clicked.connect(self.open_add_dialog)
        self.btn_add.setVisible(False)  # Скрыта, пока пользователь не авторизован как admin

        # ── Кнопка регистрации ──
        btn_register = QPushButton('Регистрация')
        btn_register.setFixedHeight(35)
        btn_register.clicked.connect(self.open_register_dialog)

        # ── Кнопка входа ──
        self.btn_login = QPushButton('Вход')
        self.btn_login.setFixedHeight(35)
        self.btn_login.clicked.connect(self.open_login_dialog)

        top_layout.addWidget(self.search_input)
        top_layout.addWidget(btn_clear)
        top_layout.addWidget(self.btn_filter)
        top_layout.addWidget(self.btn_favorites)
        top_layout.addWidget(self.btn_add)
        top_layout.addWidget(btn_register)
        top_layout.addWidget(self.btn_login)
        main_layout.addLayout(top_layout)

        # ── Метка авторизованного пользователя ──
        self.user_label = QLabel('')
        self.user_label.setStyleSheet('color: green; font-size: 11px; font-weight: bold;')
        main_layout.addWidget(self.user_label)

        # ── Метка активного фильтра ──
        self.filter_label = QLabel('')
        self.filter_label.setStyleSheet('color: blue; font-size: 11px;')
        main_layout.addWidget(self.filter_label)

        # ── Счётчик ──
        self.count_label = QLabel()
        self.count_label.setStyleSheet('color: gray; font-size: 11px;')
        main_layout.addWidget(self.count_label)

        # ── Таблица ──
        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().setStretchLastSection(True)

        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

        self.apply_filters()

    # ─────────────────── фильтрация ───────────────────

    def apply_filters(self):
        name_text = self.search_input.text().strip() or None
        kw_ids    = self.active_keyword_ids or None

        # Если включен фильтр избранного и пользователь авторизован
        if self.show_favorites_only and self.current_user:
            data = db.get_user_favorites(self.current_user['id'])
            # Применяем дополнительные фильтры к избранному
            if name_text:
                data = [p for p in data if name_text.lower() in p['nazvanie'].lower()]
            if kw_ids:
                filtered = []
                for p in data:
                    prog_kw = [kw.strip() for kw in p.get('keywords', '').split(',')]
                    all_kw = dict(db.get_all_keywords())
                    for kid in kw_ids:
                        if all_kw.get(kid) in prog_kw:
                            filtered.append(p)
                            break
                data = filtered
        elif name_text is None and kw_ids is None:
            data = db.get_all_programs()
        else:
            data = db.filter_programs(name=name_text, keyword_ids=kw_ids)

        self.load_table(data)

        if self.active_keyword_ids:
            all_kw = dict(db.get_all_keywords())
            names  = [all_kw[kid] for kid in self.active_keyword_ids if kid in all_kw]
            self.filter_label.setText('Фильтр: ' + ', '.join(names))
            self.btn_filter.setText('Фильтр ✔')
        else:
            self.filter_label.setText('')
            self.btn_filter.setText('Фильтр')

    # ─────────────────── таблица ───────────────────

    def load_table(self, data):
        self.table.setRowCount(0)
        
        # Если пользователь авторизован — добавляем колонку "Избранное"
        if self.current_user:
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(
                ['Название', 'Описание', 'Ключевые слова', 'Снимок', '☆']
            )
            self.table.setColumnWidth(0, 160)
            self.table.setColumnWidth(1, 260)
            self.table.setColumnWidth(2, 200)
            self.table.setColumnWidth(3, 220)
            self.table.setColumnWidth(4, 50)  # Колонка для избранного
        else:
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels(
                ['Название', 'Описание', 'Ключевые слова', 'Снимок']
            )
            self.table.setColumnWidth(0, 160)
            self.table.setColumnWidth(1, 260)
            self.table.setColumnWidth(2, 200)
            self.table.setColumnWidth(3, 220)

        for row, prog in enumerate(data):
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(prog['nazvanie'] or ''))
            self.table.setItem(row, 1, QTableWidgetItem(prog['opisanie'] or ''))

            # ── ключевые слова ──
            kw_text = prog.get('keywords', '') or '—'
            item_kw = QTableWidgetItem(kw_text)
            item_kw.setToolTip(kw_text)          # подсказка при наведении
            self.table.setItem(row, 2, item_kw)

            # ── скриншоты ──
            pixmap = self._load_pixmap(prog['img_data'], prog['img'])

            if pixmap and not pixmap.isNull():
                pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                label = QLabel()
                label.setPixmap(pixmap)
                label.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(row, 3, label)
                self.table.setRowHeight(row, 160)
            else:
                self.table.setItem(row, 3, QTableWidgetItem(prog['img'] or '—'))
                self.table.setRowHeight(row, 30)

            # ── звёздочка избранного ──
            if self.current_user:
                btn_star = QPushButton('В избранное')
                btn_star.setFixedSize(130, 30)
                btn_star.setStyleSheet('font-size: 18px;')
                
                # Проверяем, есть ли программа в избранном
                is_fav = db.is_in_favorites(self.current_user['id'], prog['id'])
                if is_fav:
                    btn_star.setText('★')
                    btn_star.setStyleSheet('font-size: 18px; color: gold;')
                
                # Сохраняем id программы в кнопке
                btn_star.setProperty('program_id', prog['id'])
                btn_star.setProperty('row', row)
                btn_star.clicked.connect(self.on_favorite_clicked)
                
                self.table.setCellWidget(row, 4, btn_star)
                #self.table.setRowHeight(row, 50)

        self.count_label.setText(f'Найдено записей: {len(data)}')

    def _load_pixmap(self, img_data, img_filename):
        pixmap = QPixmap()
        if img_data:
            pixmap.loadFromData(bytes(img_data))
            if not pixmap.isNull():
                return pixmap
        if img_filename:
            path = f"/home/student/Документы/Жданов/Приложение/imgs/{img_filename}"
            pixmap.load(path)
        return pixmap

    # ─────────────────── слоты ───────────────────

    def clear_search(self):
        self.search_input.clear()

    def open_filter_dialog(self):
        dialog = FilterDialog(
            previously_selected=self.active_keyword_ids,
            parent=self
        )
        if dialog.exec_() == QDialog.Accepted:
            self.active_keyword_ids = dialog.selected_ids
            self.apply_filters()

    def open_add_dialog(self):
        dialog = AddDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.apply_filters()

    def open_register_dialog(self):
        """Открывает окно регистрации пользователя"""
        dialog = RegisterDialog()
        dialog.exec_()

    def open_login_dialog(self):
        """Открывает окно авторизации пользователя"""
        dialog = LoginDialog()
        if dialog.exec_() == QDialog.Accepted:
            # Сохраняем данные пользователя
            self.current_user = {
                'login': dialog.user_login,
                'role': dialog.user_role,
                'id': dialog.user_data['id']
            }
            # Обновляем метку пользователя
            self.user_label.setText(f'{self.current_user["login"]} (роль: {self.current_user["role"]})')
            # Меняем текст кнопки на "Выход"
            self.btn_login.setText('Выход')
            self.btn_login.clicked.disconnect()
            self.btn_login.clicked.connect(self.logout)

            # Активируем кнопку избранного (для всех авторизованных)
            self.btn_favorites.setEnabled(True)
            
            # Показываем кнопку добавления только для admin
            if self.current_user['role'] == 'admin':
                self.btn_add.setVisible(True)

            # Перезагружаем таблицу со звёздочками
            self.apply_filters()

    def logout(self):
        """Выполняет выход пользователя"""
        self.current_user = None
        self.user_label.setText('')
        self.btn_login.setText('Вход')
        self.btn_login.clicked.disconnect()
        self.btn_login.clicked.connect(self.open_login_dialog)

        # Отключаем фильтр избранного и скрываем звёздочки
        self.show_favorites_only = False
        self.btn_favorites.setEnabled(False)
        self.btn_favorites.setText('☆ Избранное')
        self.btn_add.setVisible(False)  # Скрываем кнопку добавления
        self.apply_filters()

    def toggle_favorites_filter(self):
        """Переключает фильтр избранного"""
        self.show_favorites_only = not self.show_favorites_only
        
        if self.show_favorites_only:
            self.btn_favorites.setText('★ Избранное')
        else:
            self.btn_favorites.setText('☆ Избранное')
        
        self.apply_filters()

    def on_favorite_clicked(self):
        """Обработка клика на звёздочку избранного"""
        button = self.sender()
        program_id = button.property('program_id')
        row = button.property('row')
        
        if not self.current_user:
            return
        
        user_id = self.current_user['id']
        
        # Проверяем текущее состояние
        is_fav = db.is_in_favorites(user_id, program_id)
        
        if is_fav:
            # Удаляем из избранного
            db.remove_from_favorites(user_id, program_id)
            button.setText('☆')
            button.setStyleSheet('font-size: 18px;')
        else:
            # Добавляем в избранное
            db.add_to_favorites(user_id, program_id)
            button.setText('★')
            button.setStyleSheet('font-size: 18px; color: gold;')