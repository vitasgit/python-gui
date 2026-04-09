#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from window import Window
from db_login_dialog import DBLoginDialog


def setup_database(db_info):
    """Создаёт БД programms и все таблицы, если их нет"""
    
    # --- Шаг 1: подключаемся к системной БД postgres ---
    db = QSqlDatabase.addDatabase('QPSQL', 'setup_connection')
    db.setHostName(db_info['host'])
    db.setDatabaseName('postgres')  # системная БД
    db.setPort(db_info['port'])
    db.setUserName(db_info['user'])
    db.setPassword(db_info['password'])
    
    if not db.open():
        QMessageBox.critical(None, 'Ошибка', 'Не удалось подключиться к серверу PostgreSQL')
        return False
    
    # --- Шаг 2: проверяем, существует ли БД programms ---
    q = QSqlQuery(db)
    q.exec_("select 1 from pg_database where datname = 'programms'")
    
    if not q.next():
        # БД нет — создаём её
        q.exec_("create database programms")
        print("База данных 'programms' создана")
    
    db.close()
    QSqlDatabase.removeDatabase('setup_connection')
    
    # --- Шаг 3: подключаемся к БД programms ---
    db = QSqlDatabase.addDatabase('QPSQL')
    db.setHostName(db_info['host'])
    db.setDatabaseName('programms')
    db.setPort(db_info['port'])
    db.setUserName(db_info['user'])
    db.setPassword(db_info['password'])
    
    if not db.open():
        QMessageBox.critical(None, 'Ошибка', 'Не удалось подключиться к базе данных programms')
        return False
    
    # --- Шаг 4: создаём таблицы, если их нет ---
    q = QSqlQuery(db)
    
    # Таблица программ
    q.exec_("""
        create table if not exists prog (
            id serial primary key,
            nazvanie text,
            opisanie text,
            god_osnovania integer,
            img text,
            img_data bytea
        )
    """)
    
    # Таблица ключевых слов
    q.exec_("""
        create table if not exists public."Slova" (
            id serial primary key,
            nazvanie text
        )
    """)
    
    # Таблица связи программ и ключевых слов
    q.exec_("""
        create table if not exists public."Slova_Programms" (
            id_slovo integer,
            id_programm integer,
            primary key (id_slovo, id_programm),
            foreign key (id_slovo) references public."Slova"(id),
            foreign key (id_programm) references prog(id)
        )
    """)
    
    # Таблица пользователей
    q.exec_("""
        create table if not exists public."users" (
            id serial primary key,
            login text unique,
            password text,
            role text
        )
    """)
    
    # Таблица избранного
    q.exec_("""
        create table if not exists public."izbrannoe" (
            id_prog integer,
            id_user integer,
            primary key (id_prog, id_user),
            foreign key (id_prog) references prog(id),
            foreign key (id_user) references public."users"(id)
        )
    """)
    
    print("Все таблицы созданы или уже существуют")
    return True


def main():
    app = QApplication(sys.argv)

    # Сначала показываем окно авторизации к БД
    db_dialog = DBLoginDialog()
    if db_dialog.exec_() != 1:
        # Пользователь нажал "Отмена" — выходим
        sys.exit(0)

    # Получаем данные подключения от пользователя
    db_info = db_dialog.db_data

    # Создаём БД и таблицы, если их нет
    if not setup_database(db_info):
        print("Ошибка создания базы данных")
        sys.exit(1)

    # Если подключение прошло успешно — запускаем главное окно
    win = Window()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
