import sqlite3 as sl
import json

"""
SELECT ('столбцы или * для выбора всех столбцов; обязательно')
FROM ('таблица; обязательно')
WHERE ('условие/фильтрация, например, city = 'Moscow'; необязательно')
GROUP BY ('столбец, по которому хотим сгруппировать данные; необязательно')
HAVING ('условие/фильтрация на уровне сгруппированных данных; необязательно')
ORDER BY ('столбец, по которому хотим отсортировать вывод; необязательно')

"""

con = sl.connect('ready5.db')

with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS Trip (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            company INTEGER,
            plane VARCHAR,
            town_from VARCHAR,
            town_to VARCHAR,
            time_out DATETIME,
            time_in DATETIME
        );
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS Compant (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name VARCHAR
        );
     """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS Pass_in_trip (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            trip INTEGER,
            passenger INTEGER,
            place VARCHAR
        );
     """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS Pass_in_trip (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name VARCHAR
        );
    """)



#табличка
def create_tables():
    conn = sl.connect('airport.db')
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Geolocation (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                continent VARCHAR,
                coordinates VARCHAR,
                elevation_ft INT
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS Code_list (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                iso_country VARCHAR,
                iso_region VARCHAR,
                local_code VARCHAR,
                gps_code VARCHAR,
                iata_code VARCHAR,
                ident VARCHAR
            );
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS Airhub (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                municipality VARCHAR,
                name VARCHAR,
                type VARCHAR,
                id_geolocation INT,
                id_codelist INT
            );
        """)

con1 = sl.connect('airport_data.db')
def import_data_from_json(filename):
    with con1:
        cur = con1.cursor()
        with open(filename, 'r') as file:
            data = json.load(file)
        for item in data:
            #Geolocation
            cur.execute("INSERT INTO Geolocation (continent, coordinates, elevation_ft) VALUES (?, ?, ?)",
                        (item.get('continent'), item.get('coordinates'), item.get('elevation_ft')))

            #Code_list
            cur.execute(
                "INSERT INTO Code_list (iso_country, iso_region, local_code, gps_code, iata_code, ident) VALUES (?, ?, ?, ?, ?, ?)",
                (item.get('iso_country'), item.get('iso_region'), item.get('local_code'), item.get('gps_code'),
                 item.get('iata_code'), item.get('ident')))

            #Airhub
            cur.execute(
                "INSERT INTO Airhub (municipality, name, type, id_geolocation, id_codelist) VALUES (?, ?, ?, ?, ?)",
                (item.get('municipality'), item.get('name'), item.get('type'), cur.lastrowid - 2, cur.lastrowid - 1))


# Выведите принтом все вертолетные аэропорты
def print_helicopter_airports():
    with con1:
        cur = con1.cursor()
        cur.execute("SELECT name FROM Airhub WHERE type = 'heliport'")
        rows = cur.fetchall()
        for row in rows:
            print(row[0])


# Напишите функцию принимающую диапазон координат (x1,y1,x2,y2, type = None)
# если type не введен - выводящую все виды аэропортов
# если type введен выодящие только аэропорты такогоже типа
def filter_airports_by_coordinates(x1, y1, x2, y2, type_airport):
    with con1:
        cur = con1.cursor()
        if type_airport is not None:
            cur.execute("SELECT name FROM Airhub WHERE type = type_airport")
        else:
            cur.execute("SELECT name FROM Airhub")
        rows = cur.fetchall()
        for row in rows:
            print(row[0])




# sql_insert = "INSERT OR IGNORE INTO SMTH (name, age, information, tel) values(?, ?, ?, ?)"
# # INSERT OR IGNORE - модификатор для уникальных значений
# with con:
#     con.execute(sql_insert, ["человек", 20, "qweewq", "+7123321123321"])
#     # executemany - для двумерного
#     con.execute(sql_insert, ["человек2", 24, "qweewq", "+7123321123322"])
#
# with con:
#     data = con.execute("SELECT * FROM SMTH WHERE age <= 20")
#     print(data)
#     print(data.fetchall())
#     # fetchone