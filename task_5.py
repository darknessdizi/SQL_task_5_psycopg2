import psycopg2


def del_table(cursor, title=None):

    '''Функция удаляет таблицу из базы данных. Необходимо передать
    
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
                    email VARCHAR,
                    clients_id INTEGER REFERENCES Clients (id));'''
                    )
    cursor.execute('''CREATE TABLE IF NOT EXISTS Phones(
                    id SERIAL PRIMARY KEY,
                    phone VARCHAR(16),
                    clients_id INTEGER REFERENCES Clients (id));'''
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

    if my_dict['email'] != None:
        for element in my_dict['email']:
            cursor.execute('''INSERT INTO Emails(email, clients_id)
                            VALUES (%s, %s);''', (
                                element, str(id)
                                )
                            )
    if my_dict['phone'] != None:
        for element in my_dict['phone']:
            cursor.execute('''INSERT INTO Phones(phone, clients_id)
                            VALUES (%s, %s);''', (
                                element, str(id)
                                )
                            )                   
    
def add_phone(cursor, name, last_name, phone):

    '''Функция добавляет телефон к существующему клиенту. 
    
    Необходимо передать курсор, name и last_name клиента, 
    
    новый телефон.
    
    '''
    
    cursor.execute('''SELECT id FROM Clients c
                    WHERE c.name = %s AND c.last_name = %s;''', (
                        name, last_name)
                    )
    id = cursor.fetchone()
    if not id:
        print(f'Клиент {name} {last_name} не найден/на!')
    else:
        cursor.execute('''INSERT INTO Phones(phone, clients_id)
                        VALUES (%s, %s);''', (
                            phone, str(id[0])
                            )
                        )

def update_client():
    pass

def delete_phone(cursor, phone):

    '''Функция удаляет телефон у существующего клиента. 
    
    Необходимо передать курсор и номер удаляемого телефона.
    
    '''

    # cursor.execute(f'''DELETE FROM Phones
    #                 WHERE phone = {phone};''')
    cursor.execute('''DELETE FROM Phones
                    WHERE phone=%s;''', phone)


def delete_client():
    pass

def find_client(name, last_name, email, phone):
    pass


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
        # del_table(cursor, 'emails')
        # del_table(cursor, 'Phones')
        # del_table(cursor, 'Clients')
        del_table(cursor)

        create_table(cursor)

        for element in list_for_test:
            add_new_client(cursor, **element)

        add_phone(cursor, 'Dmitriy', 'Krutikov', '8(345)568-23-45')
        add_phone(cursor, 'Yana', 'Stroynaya', '+7(222)456-12-23')
        # add_phone(cursor, 'Dmitriy', 'Krutikov', '8(345)568-23-45-888') #кроме try except как еще отслеживать?????

        new_client = {'name': 'Vironika', 'last_name': 'Smit', 'email': [], 
            'phone': None}
        add_new_client(cursor, **new_client)
        add_new_client(cursor, name='Dizi', last_name='Hohotushka', 
                        email=None, phone=['+7(911)451-67-92'])

        delete_phone(cursor, '8(345)568-23-45')

        conn.commit()

    conn.close()