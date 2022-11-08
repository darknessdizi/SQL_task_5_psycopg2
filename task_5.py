import psycopg2


def del_table(cursor, title=None):

    '''Функция удаляет таблицу(цы) из базы данных. Необходимо передать
    
    курсор и название таблицы.
    
    '''

    if title:
        cursor.execute(f'''DROP TABLE {title};''')
        # cursor.execute('''DROP TABLE %s;''', title) # ???????????? почему так не работает ???????????
        # 'not all arguments converted during string formatting' ??????
    else:
        cursor.execute('''DROP TABLE Emails, Phones, Clients;''')

def create_table(cursor):

    '''Функция создает таблицы для базы данных. 
    
    Необходимо передать курсор.

    '''

    cursor.execute('''CREATE TABLE IF NOT EXISTS Clients(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(20) NOT NULL,
                    last_name VARCHAR(20) NOT NULL);'''
                    )
    cursor.execute('''CREATE TABLE IF NOT EXISTS Emails(
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(24),
                    clients_id INTEGER REFERENCES Clients (id)
                    ON DELETE CASCADE);'''
                    )
    cursor.execute('''CREATE TABLE IF NOT EXISTS Phones(
                    id SERIAL PRIMARY KEY,
                    phone VARCHAR(16),
                    clients_id INTEGER REFERENCES Clients (id)
                    ON DELETE CASCADE);'''
                    )

def add_new_client(cursor, **my_dict):

    '''Функция добавляет нового клиента. Необходимо передать курсор 
    
    и словарь с параметрами 'name': 'строка', 'last_name': 'строка', 
    
    'email': None или список 'строк', 'phone': None или список 'строк'
    
    '''

    cursor.execute('''INSERT INTO Clients(name, last_name)
                    VALUES (%s, %s) RETURNING id;''', (
                        my_dict['name'], 
                        my_dict['last_name']
                        )
                    )
    id = cursor.fetchone()[0]

    if not my_dict['email'] is None:
        for element in my_dict['email']:
            cursor.execute('''INSERT INTO Emails(email, clients_id)
                            VALUES (%s, %s);''', (element, str(id))
                            )
    if not my_dict['phone'] is None:
        for element in my_dict['phone']:
            cursor.execute('''INSERT INTO Phones(phone, clients_id)
                            VALUES (%s, %s);''', (element, str(id))
                            )                   
    
def add_phone(cursor, id, phone):

    '''Функция добавляет телефон к существующему клиенту. 
    
    Необходимо передать курсор, id клиента и новый телефон.
    
    '''
    
    cursor.execute('''INSERT INTO Phones(phone, clients_id)
                    VALUES (%s, %s);''', (phone, id))

def update_client(
    cursor, id_client, name=None, last_name=None, email=None, phone=None
    ):

    '''Функция обновляет данные на клиента. Необходимо передать курсор,
    
    id клиента и обновленные данные клиента (name, last_name, 
    
    email: 'список адресов', phone: 'список телефонов'.) В случае 

    указывания email или phone старые данные будут удалены и заменены

    на новые.
    
    '''
    
    if name or last_name:
        line = []
        if name:
            line.append(f"name = '{name}'")
        if last_name:
            line.append(f"last_name = '{last_name}'")
        line = ','.join(line)
        cursor.execute(f'''UPDATE Clients c SET {line} 
                        WHERE c.id = {id_client};''')
    if email:
        cursor.execute('''DELETE FROM Emails 
                        WHERE clients_id = %s;''', id_client)
        for element in email:
            cursor.execute('''INSERT INTO Emails (email, clients_id) 
                            VALUES (%s, %s);''', (element, id_client))
    if phone:
        cursor.execute('''DELETE FROM Phones 
                        WHERE clients_id = %s;''', id_client)
        for element in phone:
            cursor.execute('''INSERT INTO Phones (phone, clients_id) 
                            VALUES (%s, %s);''', (element, id_client))

def delete_phone(cursor, id, phone):

    '''Функция удаляет телефон у существующего клиента. 
    
    Необходимо передать курсор, id номер клиента и номер
    
    удаляемого телефона.
    
    '''

    cursor.execute('''DELETE FROM Phones
                    WHERE clients_id = %s AND phone=%s;''', (id, phone)) 


def delete_client(cursor, id):

    '''Функция удаляет клиента. Необходимо передать курсор
    
    и id номер клиента.
    
    '''

    cursor.execute('''DELETE FROM Clients
                    WHERE id = %s;''', id)

def find_client(cursor, name=None, last_name=None, email=None, phone=None):

    '''Функция ищет клиентов в базе. Необходимо передать курсор и 
    
    параметры поиска (name, last_name, email, phone). Если параметры 
    
    поиска не переданы, тогда будут напечатаны все данные из базы 
    
    данных.
    
    '''
    
    if ((name is None) and (last_name is None) and 
        (email is None) and (phone is None)):
        cursor.execute('''SELECT c.id, c.name, c.last_name, e.email, p.phone 
                        FROM Clients c
                        FULL JOIN Emails e ON e.clients_id = c.id
                        FULL JOIN Phones p ON p.clients_id = c.id 
                        ORDER  BY c.id;''')
    else:
        cursor.execute('''SELECT c.id, c.name, c.last_name, e.email, p.phone 
                        FROM Clients c
                        FULL JOIN Emails e ON e.clients_id = c.id
                        FULL JOIN Phones p ON p.clients_id = c.id
                        WHERE c.name = %s OR c.last_name = %s OR e.email = %s 
                            OR p.phone = %s 
                        ORDER  BY c.id;''', (name, last_name, email, phone))
    n = ' '
    print(f"ID{n*3}Name{n*11}Last_name{n*16}Email{n*20}Phone")
    n = 5
    for element in cursor.fetchall():
        for i in element:
            print(str(i).ljust(n, ' '), end='')
            if n == 5:
                n += 10
            elif n == 15:
                n += 10 
        print()
        n = 5
    print('-'*90)


if __name__ == '__main__':
    # создание соединения с базой данных
    conn = psycopg2.connect(
        database='task_5_db', user='postgres', password='1qaz2wsx'
        )

    # набор клиентов для наполнения базы данных
    list_for_test = [
        {'name': 'Dmitriy', 'last_name': 'Ivanov', 
            'email': ['bingo@mail.ru'], 'phone': ['+7(907)456-89-34']},
        {'name': 'Valera', 'last_name': 'Petrov', 
            'email': ['sobaken@mail.ru'], 'phone': ['+7(932)231-89-67']},
        {'name': 'Tanya', 'last_name': 'Krasavchikova', 
            'email': ['kiss_love@mail.ru'], 'phone': None},
        {'name': 'Liza', 'last_name': 'Ivanova', 'email': None,
            'phone': ['+7(907)456-89-34', '8(999)444-67-89']},
        {'name': 'Elena', 'last_name': 'Umnichkova', 
            'email': ['len4ik@mail.ru'], 'phone': ['+7(907)456-89-34']},
        {'name': 'Dmitriy', 'last_name': 'Krutikov', 
            'email': None, 'phone': None}
    ]

    with conn.cursor() as cursor:
        # удаление таблиц из базы (можно по отдельности или сразу все):
        del_table(cursor, 'Emails')
        del_table(cursor, 'Phones')
        del_table(cursor, 'Clients')
        # del_table(cursor)

        # создание таблиц для базы данных согласно заданию:
        create_table(cursor)

        # наполнение базы данных клиентами
        for element in list_for_test:
            add_new_client(cursor, **element)
        
        # вывод созданной базы даннных со списком клиентов:
        print('Созданная база данных, список клиентов:')
        find_client(cursor)

        # добавление телефонов для существующх клиентов:
        add_phone(cursor, '6', '+7(555)321-12-21')
        add_phone(cursor, '6', '8(345)568-23-45')
        add_phone(cursor, '1', '8(121)432-67-99')
        add_phone(cursor, '1', '+7(767)144-12-12')
        print('Добавлены телефоны у клиентов под номерами 6 и 1:')
        find_client(cursor)

        # добавление нового клиента 1-й способ (через словарь):
        new_client = {'name': 'Vironika', 'last_name': 'Smit', 'email': None, 
            'phone': None}
        add_new_client(cursor, **new_client)

        # добавление нового клиента 2-й способ (через именованные аргументы):
        add_new_client(cursor, name='Izi', last_name='Love', 
                        email=['jzlk_milk@mail.ru', 'izi_live@mail.ru'], 
                        phone=None)
        add_new_client(cursor, name='Vika', last_name='Best', 
                        email=None, phone=None)
        print('Добавлены три новых клиента:')
        find_client(cursor)

        # поиск клиента по параметрам:
        print('Поиск по номеру телефона:')
        find_client(cursor, phone='+7(932)231-89-67')
        print('Поиск по имени:')
        find_client(cursor, name='Liza')
        print('Поиск по фамилии и email:')
        find_client(cursor, last_name='Smit', email='len4ik@mail.ru')

        # обновление данных на клиента:
        update_client(cursor, '6', last_name='Bratislavovich', 
                      phone=['+7(333)333-33-33', '+7(555)321-12-21'])
        update_client(cursor, '4', email=['sweets@mail.ru'])
        update_client(cursor, '5', name='Alisa', last_name='Veselushka')
        print('Обновлены данные у клиентов под номерами 4, 5 и 6:')
        find_client(cursor)

        # удаление номера телефона у существующего клиента:
        delete_phone(cursor, '4', '+7(907)456-89-34')
        delete_phone(cursor, '6', '+7(555)321-12-21')
        print('Удалены по 1 телефону у клиентов под номерами 4 и 6:')
        find_client(cursor)

        # удаление клиентов (каскадное удаление их email и phone):
        delete_client(cursor, '1')
        delete_client(cursor, '8')
        print('Удалены клиенты под номерами 1 и 8:')
        find_client(cursor)

        conn.commit()

    conn.close()