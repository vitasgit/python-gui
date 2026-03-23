from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QByteArray


KEYWORDS_SUBQUERY = '''
    (SELECT COALESCE(string_agg(s2.nazvanie, ', ' ORDER BY s2.nazvanie), '')
     FROM public."Slova_Programms" sp2
     JOIN public."Slova" s2 ON s2.id = sp2.id_slovo
     WHERE sp2.id_programm = prog.id)
'''


def get_all_programs():
    q = QSqlQuery()
    q.exec_(f'''
        SELECT prog.id, prog.nazvanie, prog.opisanie,
               prog.god_osnovania, prog.img, prog.img_data,
               {KEYWORDS_SUBQUERY} AS keywords
        FROM prog
        ORDER BY prog.nazvanie
    ''')

    results = []
    while q.next():
        results.append({
            'id':             q.value(0),
            'nazvanie':       q.value(1),
            'opisanie':       q.value(2),
            'god_osnovania':  q.value(3),
            'img':            q.value(4),
            'img_data':       q.value(5),
            'keywords':       q.value(6),
        })
    return results


def filter_programs(name=None, keyword_ids=None):
    base = f'''
        SELECT DISTINCT
            prog.id, prog.nazvanie, prog.opisanie,
            prog.god_osnovania, prog.img, prog.img_data,
            {KEYWORDS_SUBQUERY} AS keywords
        FROM prog
    '''

    conditions = []

    if keyword_ids:
        base += '''
            JOIN public."Slova_Programms" sp ON sp.id_programm = prog.id
        '''
        id_list = ','.join(str(int(kid)) for kid in keyword_ids)
        conditions.append(f'sp.id_slovo IN ({id_list})')

    if name:
        conditions.append('prog.nazvanie ILIKE :name')

    if conditions:
        base += ' WHERE ' + ' AND '.join(conditions)

    base += ' ORDER BY prog.nazvanie'

    q = QSqlQuery()
    q.prepare(base)

    if name:
        q.bindValue(':name', f'%{name}%')

    q.exec_()

    results = []
    while q.next():
        results.append({
            'id':             q.value(0),
            'nazvanie':       q.value(1),
            'opisanie':       q.value(2),
            'god_osnovania':  q.value(3),
            'img':            q.value(4),
            'img_data':       q.value(5),
            'keywords':       q.value(6),
        })
    return results


def get_all_keywords():
    q = QSqlQuery()
    q.exec_('SELECT id, nazvanie FROM public."Slova" ORDER BY nazvanie')

    results = []
    while q.next():
        results.append((q.value(0), q.value(1)))
    return results


def add_keyword(nazvanie):
    """Добавляет новое ключевое слово в таблицу Slova и возвращает его id"""
    q = QSqlQuery()
    q.prepare('''
        INSERT INTO public."Slova" (nazvanie)
        VALUES (:nazvanie)
        RETURNING id
    ''')
    q.bindValue(':nazvanie', nazvanie)
    
    if not q.exec_():
        return None
    
    q.next()
    return q.value(0)


def add_program(nazvanie, opisanie, god_osnovania, img_filename, img_bytes, keyword_ids):
    q = QSqlQuery()
    q.prepare('''
        INSERT INTO prog (nazvanie, opisanie, god_osnovania, img, img_data)
        VALUES (:name, :desc, :date, :img, :img_data)
        RETURNING id
    ''')
    q.bindValue(':name', nazvanie)
    q.bindValue(':desc', opisanie)
    q.bindValue(':date', god_osnovania if god_osnovania else None)

    if img_bytes:
        q.bindValue(':img', img_filename)
        q.bindValue(':img_data', QByteArray(img_bytes))
    else:
        q.bindValue(':img', None)
        q.bindValue(':img_data', None)

    if not q.exec_():
        return False

    q.next()
    new_id = q.value(0)

    for kw_id in keyword_ids:
        q2 = QSqlQuery()
        s = f"""INSERT INTO public."Slova_Programms" (id_slovo, id_programm)
                VALUES ({kw_id}, {new_id})"""
        q2.exec_(s)

    return True