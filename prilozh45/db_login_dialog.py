from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox
)
from PyQt5.QtSql import QSqlDatabase


class DBLoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Подключение к базе данных')
        self.setFixedSize(400, 250)

        # Данные подключения (заполняются после нажатия кнопки)
        self.db_data = None

        # Основной вертикальный макет
        main_layout = QVBoxLayout()

        # Форма с полями ввода
        form = QFormLayout()

        # Поле: Имя базы данных
        self.input_db_name = QLineEdit()
        self.input_db_name.setText('programms')
        form.addRow('Имя БД:', self.input_db_name)

        # Поле: Имя пользователя
        self.input_user = QLineEdit()
        self.input_user.setText('postgres')
        form.addRow('Имя пользователя:', self.input_user)

        # Поле: Порт
        self.input_port = QLineEdit()
        self.input_port.setText('5432')
        form.addRow('Порт БД:', self.input_port)

        # Поле: Hostname
        self.input_host = QLineEdit()
        self.input_host.setText('localhost')
        form.addRow('Hostname:', self.input_host)

        # Поле: Пароль (скрываем символы)
        self.input_password = QLineEdit()
        self.input_password.setText('123456')
        self.input_password.setEchoMode(QLineEdit.Password)
        form.addRow('Пароль:', self.input_password)

        main_layout.addLayout(form)

        # Кнопки
        btn_layout = QHBoxLayout()
        btn_connect = QPushButton('Подключиться')
        btn_cancel = QPushButton('Отмена')

        btn_connect.clicked.connect(self.try_connect)
        btn_cancel.clicked.connect(self.reject)

        btn_layout.addWidget(btn_connect)
        btn_layout.addWidget(btn_cancel)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    def try_connect(self):
        """Пытается подключиться к БД с введёнными данными"""
        # Получаем данные из полей ввода
        dbname = self.input_db_name.text().strip()
        user = self.input_user.text().strip()
        port = self.input_port.text().strip()
        host = self.input_host.text().strip()
        password = self.input_password.text().strip()

        # Проверка: все поля должны быть заполнены
        if not dbname:
            QMessageBox.warning(self, 'Ошибка', 'Введите имя базы данных')
            return

        if not user:
            QMessageBox.warning(self, 'Ошибка', 'Введите имя пользователя')
            return

        if not port:
            QMessageBox.warning(self, 'Ошибка', 'Введите порт БД')
            return

        if not host:
            QMessageBox.warning(self, 'Ошибка', 'Введите hostname')
            return

        if not password:
            QMessageBox.warning(self, 'Ошибка', 'Введите пароль')
            return

        # Проверяем, что порт — это число
        try:
            port_int = int(port)
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Порт должен быть числом')
            return

        # Создаём подключение к БД
        db = QSqlDatabase.addDatabase('QPSQL')
        db.setHostName(host)
        db.setDatabaseName(dbname)
        db.setPort(port_int)
        db.setUserName(user)
        db.setPassword(password)

        # Пробуем открыть соединение
        if not db.open():
            # Ошибка подключения
            QMessageBox.critical(
                self,
                'Ошибка подключения',
                'Не удалось подключиться к базе данных.\n\n' + db.lastError().text()
            )
            return

        # Сохраняем данные подключения
        self.db_data = {
            'dbname': dbname,
            'user': user,
            'port': port_int,
            'host': host,
            'password': password,
        }

        # Закрываем окно (успех)
        self.accept()
