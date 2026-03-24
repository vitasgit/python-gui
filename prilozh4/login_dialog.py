from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox
)
import db


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Вход')
        self.setFixedSize(300, 150)

        # Основной вертикальный макет
        main_layout = QVBoxLayout()

        # Форма с полями ввода
        form = QFormLayout()

        self.input_login = QLineEdit()
        self.input_login.setPlaceholderText('Введите логин')

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText('Введите пароль')
        self.input_password.setEchoMode(QLineEdit.Password)  # Скрываем символы пароля

        form.addRow('Логин:', self.input_login)
        form.addRow('Пароль:', self.input_password)

        main_layout.addLayout(form)

        # Кнопки
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton('Вход')
        btn_cancel = QPushButton('Отмена')

        btn_ok.clicked.connect(self.login)
        btn_cancel.clicked.connect(self.reject)

        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    def login(self):
        """Проверяет логин и пароль пользователя"""
        login = self.input_login.text().strip()
        password = self.input_password.text().strip()

        # Проверка: поля не должны быть пустыми
        if not login:
            QMessageBox.warning(self, 'Ошибка', 'Введите логин')
            return

        if not password:
            QMessageBox.warning(self, 'Ошибка', 'Введите пароль')
            return

        # Проверка пользователя в БД
        user_data = db.check_user(login=login, password=password)

        if user_data:
            # Пользователь найден - сохраняем данные и закрываем окно
            self.user_login = login
            self.user_role = user_data['role']
            self.accept()
        else:
            QMessageBox.critical(self, 'Ошибка', 'Неверный логин или пароль')
