# db.py — слой данных
# Этот файл знает КАК работать с БД: какие таблицы есть, какие запросы делать.
# Окна (window.py, add_dialog.py) не пишут SQL — они вызывают функции отсюда.
# Это принцип разделения ответственности: если завтра поменяешь структуру БД,
# менять нужно будет только этот файл, а не весь интерфейс.

from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMessageBox


def get_all_programs():
    """
    Возвращает все программы из БД.
    
    Результат — список словарей, каждый словарь = одна строка.
    Например: [{'id': 1, 'nazvanie': 'GIMP', 'opisanie': '...', ...}, ...]
    
    Почему список словарей, а не просто QSqlQuery?
    Потому что так данные легче передавать между функциями и файлами.
    QSqlQuery — это "курсор", его нельзя просто передать и потом читать.
    """
    q = QSqlQuery()
    q.exec_('SELECT id, nazvanie, opisanie, god_osnovania, img, img_data FROM prog ORDER BY id')

    results = []
    while q.next():
        results.append({
            'id':            q.value(0),
            'nazvanie':      q.value(1),
            'opisanie':      q.value(2),
            'god_osnovania': q.value(3),
            'img':           q.value(4),
            'img_data':      q.value(5),  # bytes или None
        })
    return results


def search_programs(keyword):
    """
    Ищет программы у которых есть ключевое слово содержащее keyword.
    
    Алгоритм:
    1. Делаем JOIN трёх таблиц: prog → Slova_Programms → Slova
    2. Фильтруем по ILIKE (регистронезависимый LIKE в PostgreSQL)
    3. DISTINCT чтобы не было дублей (если у программы несколько подходящих слов)
    
    Пример: ищем "антивир" → найдёт программы с ключевым словом "антивирус"
    """
    q = QSqlQuery()
    # Параметризованный запрос: :kw — заполнитель для значения
    q.prepare('''
        SELECT DISTINCT
            prog.id,
            prog.nazvanie,
            prog.opisanie,
            prog.god_osnovania,
            prog.img,
            prog.img_data
        FROM prog
        JOIN public."Slova_Programms" sp ON sp.id_programm = prog.id
        JOIN public."Slova"           s  ON s.id = sp.id_slovo
        WHERE s.nazvanie ILIKE :kw
    ''')
    # % с двух сторон = "содержит" (не обязательно с начала строки)
    q.bindValue(':kw', f'%{keyword}%')
    q.exec_()

    results = []
    while q.next():
        results.append({
            'id':            q.value(0),
            'nazvanie':      q.value(1),
            'opisanie':      q.value(2),
            'god_osnovania': q.value(3),
            'img':           q.value(4),
            'img_data':      q.value(5),
        })
    return results


def get_all_keywords():
    """
    Возвращает все ключевые слова из таблицы Slova.
    Используется в диалоге добавления — показываем чекбоксы с вариантами.
    Возвращает список кортежей: [(id, nazvanie), (id, nazvanie), ...]
    """
    q = QSqlQuery()
    q.exec_('SELECT id, nazvanie FROM public."Slova" ORDER BY nazvanie')

    results = []
    while q.next():
        results.append((q.value(0), q.value(1)))
    return results


def add_program(nazvanie, opisanie, god_osnovania, img_filename, img_bytes, keyword_ids):
    """
    Добавляет новую программу в БД.
    
    Параметры:
        nazvanie      — строка
        opisanie      — строка
        god_osnovania — строка вида '1997-05-26'
        img_filename  — строка (имя файла, можно оставить для совместимости)
        img_bytes     — bytes или None (бинарные данные картинки)
        keyword_ids   — список id ключевых слов (из таблицы Slova)
    
    Алгоритм:
    1. INSERT в таблицу prog → получаем id новой записи
    2. Для каждого выбранного ключевого слова — INSERT в Slova_Programms
    
    Почему два шага?  
    Потому что это связь "многие ко многим" через промежуточную таблицу.
    Сначала создаём программу, потом привязываем к ней слова.
    """
    q = QSqlQuery()

    # Шаг 1: вставляем программу
    # RETURNING id — PostgreSQL вернёт id только что созданной записи
    q.prepare('''
        INSERT INTO prog (nazvanie, opisanie, god_osnovania, img, img_data)
        VALUES (:name, :desc, :date, :img, :img_data)
        RETURNING id
    ''')
    q.bindValue(':name',     nazvanie)
    q.bindValue(':desc',     opisanie)
    q.bindValue(':date',     god_osnovania if god_osnovania else None)
    q.bindValue(':img',      img_filename)
    q.bindValue(':img_data', img_bytes)  # Qt сам сконвертирует bytes → bytea

    if not q.exec_():
        QMessageBox.critical(None, 'Ошибка БД', q.lastError().text())
        return False

    # Читаем вернувшийся id
    q.next()
    new_id = q.value(0)

    # Шаг 2: привязываем ключевые слова
    for kw_id in keyword_ids:
        q2 = QSqlQuery()
        q2.prepare('''
            INSERT INTO public."Slova_Programms" (id_slovo, id_programm)
            VALUES (:slovo, :prog)
        ''')
        q2.bindValue(':slovo', kw_id)
        q2.bindValue(':prog',  new_id)
        if not q2.exec_():
            QMessageBox.critical(None, 'Ошибка БД', q2.lastError().text())
            return False

    return True
