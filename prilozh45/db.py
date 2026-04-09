from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QByteArray


KEYWORDS_SUBQUERY = '''
    (select coalesce(string_agg(s2.nazvanie, ', ' order by s2.nazvanie), '')
     from public."Slova_Programms" sp2
     join public."Slova" s2 on s2.id = sp2.id_slovo
     where sp2.id_programm = prog.id)
'''


def get_all_programs():
    q = QSqlQuery()
    q.exec_(f'''
        select prog.id, prog.nazvanie, prog.opisanie,
               prog.god_osnovania, prog.img, prog.img_data,
               {KEYWORDS_SUBQUERY} AS keywords
        from prog
        order by prog.nazvanie
    ''')

    results = []
    while q.next():
        results.append({
            'id': q.value(0),
            'nazvanie': q.value(1),
            'opisanie': q.value(2),
            'god_osnovania': q.value(3),
            'img': q.value(4),
            'img_data': q.value(5),
            'keywords': q.value(6),
        })
    return results


def filter_programs(name=None, keyword_ids=None):
    base = f'''
        select distinct
            prog.id, prog.nazvanie, prog.opisanie,
            prog.god_osnovania, prog.img, prog.img_data,
            {KEYWORDS_SUBQUERY} AS keywords
        from prog
    '''

    conditions = []

    if keyword_ids:
        base += '''
            join public."Slova_Programms" sp on sp.id_programm = prog.id
        '''
        id_list = ','.join(str(int(kid)) for kid in keyword_ids)
        conditions.append(f'sp.id_slovo in ({id_list})')

    if name:
        conditions.append('prog.nazvanie ilike :name')

    if conditions:
        base += ' where ' + ' and '.join(conditions)

    base += ' order by prog.nazvanie'

    q = QSqlQuery()
    q.prepare(base)

    if name:
        q.bindValue(':name', f'%{name}%')

    q.exec_()

    results = []
    while q.next():
        results.append({
            'id': q.value(0),
            'nazvanie': q.value(1),
            'opisanie': q.value(2),
            'god_osnovania': q.value(3),
            'img': q.value(4),
            'img_data': q.value(5),
            'keywords': q.value(6),
        })
    return results


def get_all_keywords():
    q = QSqlQuery()
    q.exec_('select id, nazvanie from public."Slova" order by nazvanie')

    results = []
    while q.next():
        results.append((q.value(0), q.value(1)))
    return results


def add_keyword(nazvanie):
    """Добавляет новое ключевое слово в таблицу Slova и возвращает его id"""
    q = QSqlQuery()
    q.prepare('''
        insert into public."Slova" (nazvanie)
        values (:nazvanie)
        returning id
    ''')
    q.bindValue(':nazvanie', nazvanie)

    if not q.exec_():
        return None

    q.next()
    return q.value(0)


def add_program(nazvanie, opisanie, god_osnovania, img_filename, img_bytes, keyword_ids):
    q = QSqlQuery()
    q.prepare('''
        insert into prog (nazvanie, opisanie, god_osnovania, img, img_data)
        values (:name, :desc, :date, :img, :img_data)
        returning id
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
        s = f"""insert into public."Slova_Programms" (id_slovo, id_programm)
                values ({kw_id}, {new_id})"""
        q2.exec_(s)

    return True


def add_user(login, password):
    q = QSqlQuery()
    q.prepare('''
        insert into public."users" (login, password, role)
        values (:login, :password, :role)
        returning id
    ''')
    q.bindValue(':login', login)
    q.bindValue(':password', password)
    q.bindValue(':role', 'user')  # роль по умолчанию

    if not q.exec_():
        return False

    return True


def check_user(login, password):
    q = QSqlQuery()
    q.prepare('''
        select id, login, role
        from public."users"
        where login = :login and password = :password
    ''')
    q.bindValue(':login', login)
    q.bindValue(':password', password)

    if not q.exec_():
        return None

    if q.next():
        return {
            'id': q.value(0),
            'login': q.value(1),
            'role': q.value(2),
        }
    return None


def add_to_favorites(user_id, program_id):
    q = QSqlQuery()
    q.prepare('''
        insert into public."izbrannoe" (id_prog, id_user)
        values (:id_prog, :id_user)
    ''')
    q.bindValue(':id_prog', program_id)
    q.bindValue(':id_user', user_id)

    return q.exec_()


def remove_from_favorites(user_id, program_id):
    q = QSqlQuery()
    q.prepare('''
        delete from public."izbrannoe"
        where id_prog = :id_prog and id_user = :id_user
    ''')
    q.bindValue(':id_prog', program_id)
    q.bindValue(':id_user', user_id)

    return q.exec_()


def is_in_favorites(user_id, program_id):
    """проверяем есть ли уже в избранном"""
    q = QSqlQuery()
    q.prepare('''
        select id from public."izbrannoe"
        where id_prog = :id_prog and id_user = :id_user
    ''')
    q.bindValue(':id_prog', program_id)
    q.bindValue(':id_user', user_id)

    if q.exec_() and q.next():
        return True
    return False


def get_user_favorites(user_id):
    q = QSqlQuery()
    q.exec_(f'''
        select prog.id, prog.nazvanie, prog.opisanie,
               prog.god_osnovania, prog.img, prog.img_data,
               {KEYWORDS_SUBQUERY} AS keywords
        from prog
        join public."izbrannoe" iz on iz.id_prog = prog.id
        where iz.id_user = {user_id}
        order by prog.nazvanie
    ''')

    results = []
    while q.next():
        results.append({
            'id': q.value(0),
            'nazvanie': q.value(1),
            'opisanie': q.value(2),
            'god_osnovania': q.value(3),
            'img': q.value(4),
            'img_data': q.value(5),
            'keywords': q.value(6),
        })
    return results
