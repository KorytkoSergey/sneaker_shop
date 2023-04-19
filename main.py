import psycopg2
import sys


def cross_road(key, connection):
    dct = {'insert': add_srt,
           'limit': limit_row,
           '*': show_all,
           'get': get_filter,
           'update': update_table,
           'delete': delete_row,
           'exit': sys.exit}

    if key in dct:
        return dct[key](connection)
    else:
        return dct['*'](connection)


def add_srt(connection):
    row = int(input('сколько добавляем строк?\n'))
    for x in range(row):
        brand = input('brand\n')
        model = input('model\n')
        size = float(input('size\n'))
        color = input('color\n').capitalize()
        price = float(input('price\n'))
        with connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO shop.sneakers (brand, model, sneak_size, color, price) VALUES
                            ('{brand}', '{model}', {size}, '{color}', {price});"""
            )
            print("Данные успешно добавлены")


def show_all(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM shop.sneakers;"""
        )
        rows = cursor.fetchall()
        for row in rows:
            print(row)


def limit_row(connection):
    count = int(input('Количество строк\n'))
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT * FROM shop.sneakers LIMIT {count};"""
        )

        rows = cursor.fetchall()
        for row in rows:
            print(row)


def get_filter(connection):
    marker = input('По какому столбцу выводим?\n')
    marker_value = input('Значение фильтра\n')
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT * FROM shop.sneakers WHERE {marker} = '{marker_value}';"""
        )
        print(cursor.fetchone())


def update_table(connection):
    table_id = int(input('Укажите sneak_id по которому будем изменять строку\n'))
    brand = input('brand\n')
    model = input('model\n')
    size = float(input('size\n'))
    color = input('color\n').capitalize()
    price = float(input('price\n'))
    with connection.cursor() as cursor:
        cursor.execute(
            """UPDATE shop.sneakers SET brand = %s, model = %s, sneak_size = %s, color = %s, price = %s 
            WHERE sneak_id = %s""",
            (brand, model, size, color, price, table_id)
        )
        print("Запись успешно изменена")


def delete_row(connection):
    table_id = int(input("Укажите sneak_id строки для удаления\n"))
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM shop.sneakers WHERE sneak_id = %s;
            """,
            (table_id,)
        )
        print("Запись успешно удалена")


def create_table(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE SCHEMA shop;
            """
        )
        cursor.execute(
            """CREATE TABLE shop.sneakers (
    sneak_id SERIAL PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    sneak_size DECIMAL(3,1) NOT NULL,
    color VARCHAR(20) NOT NULL,
    price DECIMAL(10,2) NOT NULL);"""
        )
        cursor.execute(
            """INSERT INTO shop.sneakers (brand, model, sneak_size, color, price) VALUES
        ('Nike', 'Air Max 90', 37.5, 'White', 120),
        ('Adidas', 'Superstar', 42, 'Black', 89.99),
        ('Puma', 'RS-2K', 38, 'Red', 109.99),
        ('New Balance', '327', 41, 'Blue', 99.00),
        ('Reebok', 'Classic Leather', 45, 'Gum', 75.00);"""
        )
        print("Таблица успешна создана")


def machina(user, password, host, port, database):
    try:
        # Устанавливаем соединение с базой данных
        connection = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
        connection.autocommit = True
        # Проверяем, что соединение установлено успешно
        if connection:
            print("Соединение установлено")
        new_table = input("Надо ли создавать тестовую таблицу? y/n\n")
        if new_table == 'y':
            create_table(connection)
        else:
            print("Надеюсь вы знаете, что вы делаете")
        door = True
        while door:
            print("Если нужна подсказка, то напишите help")
            key = input()
            if key == 'help':
                print("Что вы хотите сделать?")
                print(f'''Если хотите добавить запись в таблицу, то напишите "insert"
                Если хотите получить все строки таблицы, то напишите "*"
                Если хотите получить определенное количество строк, то напишите "limit"
                Если хотите получить запрос по sneak_id/brand/model/sneak_size/color/price, то напишите "get"
                Если хотите изменить запись в таблице, то напишите "update"
                Если хотите удалить строку в таблице, то напишите "delete"
                Если хотите завершить работу, то напишите "exit" ''')
            else:
                cross_road(key, connection)

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        # Закрываем соединение с базой данных, чтобы не занимать лишнюю память
        if connection:
            connection.close()
            print("Соединение с базой данных закрыто")

def config():
    print('Давайте подключимся к PostgreSQL')
    user = str(input("Введите имя\n"))
    password = str(input("Пароль\n"))
    host = str(input("Хост\n"))
    port = str(input("Порт\n"))
    database = str(input("Название базы данных\n"))
    machina(user, password, host, port, database)


if __name__ == '__main__':
    config()
