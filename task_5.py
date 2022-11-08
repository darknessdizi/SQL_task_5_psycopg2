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

def update_client(cursor, id_client, name=None, last_name=None, email=None, phone=None):
    line = []
    if name:
        line.append(f"name = '{name}'")
    if last_name:
        line.append(f"last_name = '{last_name}'")
    if name or last_name:
        line = ','.join(line)
        cursor.execute(f'''UPDATE Clients c SET {line} WHERE c.id = {id_client};''')
    if email:
        line = f"email= '{email}'"
        cursor.execute(f'''UPDATE Emails SET {line} WHERE clients_id = {id_client};''')
    if phone:
        line = f"phone= '{phone}'"
        cursor.execute(f'''UPDATE Phones SET {line} WHERE clients_id = {id_client};''')

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
                        WHERE c.name = %s OR c.last_name = %s OR e.email = %s OR p.phone = %s 
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
    print()


if __name__ == '__main__':
    conn = psycopg2.connect(database='task_5_db', user='postgres', password='1qaz2wsx')

    list_for_test = [
        {'name': 'Dmitriy', 'last_name': 'Ivanov', 'email': ['bingo@mail.ru'],
            'phone': ['+7(907)456-89-34']},
        {'name': 'Valera', 'last_name': 'Petrov', 'email': ['sobaken@mail.ru'], 
            'phone': ['+7(932)231-89-67']},
        {'name': 'Tanya', 'last_name': 'Krasavchikova', 'email': ['kiss_love@mail.ru'], 
            'phone': None},
        {'name': 'Liza', 'last_name': 'Ivanova', 'email': None,
            'phone': ['+7(907)456-89-34', '8(999)444-67-89']},
        {'name': 'Elena', 'last_name': 'Umnichkova', 'email': ['len4ik@mail.ru'], 
            'phone': ['+7(907)456-89-34']},
        {'name': 'Dmitriy', 'last_name': 'Krutikov', 'email': None, 
            'phone': None}
    ]

    with conn.cursor() as cursor:
        # del_table(cursor, 'Emails')
        # del_table(cursor, 'Phones')
        # del_table(cursor, 'Clients')
        # del_table(cursor)

        # create_table(cursor)

        # for element in list_for_test:
        #     add_new_client(cursor, **element)

        # add_phone(cursor, 'Dmitriy', 'Krutikov', '8(345)568-23-45')
        # add_phone(cursor, 'Dmitriy', 'Krutikov', '8(121)432-67-99')
        # add_phone(cursor, 'Dmitriy', 'Krutikov', '+7(767)144-12-12')
        # add_phone(cursor, 'Yana', 'Stroynaya', '+7(222)456-12-23')
        # add_phone(cursor, 'Dmitriy', 'Krutikov', '8(345)568-23-45-888') #кроме try except как еще отслеживать?????

        # new_client = {'name': 'Vironika', 'last_name': 'Smit', 'email': [], 
        #     'phone': None}
        # add_new_client(cursor, **new_client)
        # add_new_client(cursor, name='Izi', last_name='Penthause', 
        #                 email=['sisi@mail.ru'], phone=None)
        # add_new_client(cursor, name='Vika', last_name='Sosochkova', 
        #                 email=None, phone=None)

        # find_client(cursor, phone='+7(932)231-89-67')
        # print()
        # find_client(cursor)
        # print()
        # find_client(cursor, name='Dizi')
        # print()
        # find_client(cursor, last_name='Smit', email='len4ik@mail.ru')
        # print()
        # find_client(cursor, email='len4ik@mail.ru', last_name='Smit', name='Dmitriy')
        # print()
        update_client(cursor, '1', name='Alisa', last_name='Pervaya')
        find_client(cursor)
        # update_client(cursor, '4', name='Zayka', last_name='Shustriy', 
        #               email='darklogos@mail.ru', phone='+7(333)666-77-88')
        # update_client(cursor, '4')
        # add_phone(cursor, '12', '+7(555)321-12-21')
        # delete_phone(cursor, '4', '+7(111)444-55-66')
        # find_client(cursor, name='Demon')

        # delete_client(cursor, '3')

        conn.commit()

    conn.close()