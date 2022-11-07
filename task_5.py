import psycopg2

def del_table(cursor):
    cursor.execute('''DROP TABLE Emails, Phones, Clients;''')

def create_table(cursor):

    '''Функция создает таблицы для базы данных 

    '''

    cursor.execute('''CREATE TABLE IF NOT EXISTS Clients(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(20) NOT NULL,
                    last_name VARCHAR(20) NOT NULL
    );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Emails(
                    id SERIAL PRIMARY KEY,
                    email VARCHAR,
                    clients_id INTEGER REFERENCES Clients (id)
    );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Phones(
                    id SERIAL PRIMARY KEY,
                    phone VARCHAR(16),
                    clients_id INTEGER REFERENCES Clients (id)
    );''')

def add_new_client(cursor, **my_dict):

    '''Функция добавляет нового клиента'''

    cursor.execute('''INSERT INTO Clients(name, last_name)
                    VALUES (%s, %s) RETURNING id;''', (
                        my_dict['name'], 
                        my_dict['last_name']
                        ))
    id = cursor.fetchone()[0]

    if my_dict['email'] != None:
        cursor.execute('''INSERT INTO Emails(email, clients_id)
                        VALUES (%s, %s) RETURNING id;''', (
                            my_dict['email'], str(id)
                            ))
    if my_dict['phone'] != None:
        cursor.execute('''INSERT INTO Phones(phone, clients_id)
                        VALUES (%s, %s) RETURNING id;''', (
                            my_dict['phone'], str(id)
                            ))                   
    

def add_phone():
    pass

def update_client():
    pass

def delete_phone():
    pass

def delete_client():
    pass

def find_client(name, last_name, email, phone):
    pass


if __name__ == '__main__':
    conn = psycopg2.connect(database='task_5_db', user='postgres', password='1qaz2wsx')

    list_for_test = [
        {'name':'Dmitriy', 'last_name':'Ivanov', 'email':'bingo@mail.ru', 'phone':'+7(907)456-89-34'},
        {'name':'Valera', 'last_name':'Petrov', 'email':'sobaken@mail.ru', 'phone':'+7(932)231-89-67'},
        {'name':'Tanya', 'last_name':'Krasavchikova', 'email':'kiss_love@mail.ru', 'phone': None},
        {'name':'Liza', 'last_name':'Ivanova', 'email': None,'phone':'+7(907)456-89-34'},
        {'name':'Elena', 'last_name':'Umnichkova', 'email':'len4ik@mail.ru', 'phone':'+7(907)456-89-34'},
        {'name':'Dmitriy', 'last_name':'Krutikov', 'email': None, 'phone': None},
    ]

    with conn.cursor() as cursor:
        del_table(cursor)
        create_table(cursor)
        for element in list_for_test:
            add_new_client(cursor, **element)
        conn.commit()

    conn.close()