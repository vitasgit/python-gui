# main.py — точка входа в приложение
# Задача этого файла — две вещи:
#   1. Подключиться к БД (это должно произойти ДО создания любых окон,
#      потому что окна сразу делают запросы)
#   2. Создать приложение и показать главное окно
#
# Всё остальное — не его дело.

import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtSql import QSqlDatabase

from window import Window


def connect_db():
    """
    Подключается к PostgreSQL.
    Возвращает True если успешно, False если нет.
    
    Почему вынесено в отдельную функцию?
    Чтобы main() был читаемым: "подключись к БД, если не получилось — выйди".
    """
    db = QSqlDatabase.addDatabase('QPSQL')
    db.setHostName('localhost')
    db.setDatabaseName('programms')
    db.setPort(5432)
    db.setUserName('postgres')
    db.setPassword('123456')

    if not db.open():
        print('Ошибка подключения к БД:', db.lastError().text())
        return False
    return True


def main():
    app = QApplication(sys.argv)

    # Сначала подключаемся к БД
    if not connect_db():
        # Показываем ошибку графически (QApplication уже создан, поэтому можно)
        QMessageBox.critical(None, 'Ошибка', 'Не удалось подключиться к базе данных.\nПроверьте настройки подключения в main.py')
        sys.exit(1)

    # Всё готово — показываем главное окно
    win = Window()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    # __name__ == '__main__' означает что файл запущен напрямую (не импортирован)
    # Это стандартная защита: если кто-то сделает import main — main() не запустится сам
    main()
