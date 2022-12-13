import sqlite3
import json
from prettytable import PrettyTable


def sqlite_connect():
    try:
        sql_con = sqlite3.connect(r"D:\Курсовая работа\Программа курсовой\SQLite DataBase\Library Readers.db")
        print("База данных успешно подключена к SQLite")
        return sql_con
    except sqlite3.Error as err:
        print("Ошибка подключения базы данных", err)


def sqlite_disconnect(sql_con):
    if sql_con:
        sql_con.close()
        print("Соединение с SQLite закрыто")


def sqlite_table(sql_con):
    cursor = sql_con.cursor()
    sql = ("""

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Readers (
    id_reader INTEGER PRIMARY KEY AUTOINCREMENT
                    UNIQUE
);
CREATE TABLE IF NOT EXISTS Persons (
    id_person        INTEGER      PRIMARY KEY AUTOINCREMENT,
    id_reader_person INTEGER      REFERENCES Readers (id_reader) ON DELETE CASCADE
                                                                 ON UPDATE CASCADE,
    fio              VARCHAR (70) NOT NULL ON CONFLICT ROLLBACK,
    gender           VARCHAR (15) NOT NULL ON CONFLICT ROLLBACK,
    birthday         INTEGER      NOT NULL ON CONFLICT ROLLBACK,
    age              INTEGER      NOT NULL ON CONFLICT ROLLBACK,
    education        VARCHAR (90) NOT NULL ON CONFLICT ROLLBACK
);
CREATE TABLE IF NOT EXISTS Addresses (
    id_reader_address INTEGER       REFERENCES Readers (id_reader) ON DELETE CASCADE
                                                                   ON UPDATE CASCADE,
    address           VARCHAR (350) NOT NULL ON CONFLICT ROLLBACK
);
""")
    cursor.executescript(sql)
    sql_con.commit()
    cursor.close()


def sqlite_select(sql_con, table_name, result=None):
    output_table = PrettyTable()
    cursor = sql_con.cursor()
    if result is not None:
        sql_ex = """
            SELECT id_reader,
            fio, gender, birthday, age, education,
            address
            FROM Readers
            
            LEFT JOIN 
            Persons on Readers.id_reader = Persons.id_reader_person
            
            LEFT JOIN
            Addresses on Addresses.id_reader_address = Readers.id_reader;
        """
        cursor.execute(sql_ex)
        rows = cursor.fetchall()
        output_table.field_names = ["Номер читательского билета", "ФИО",
                                    "Пол", "День рождения", "Возраст", "Образование",
                                    "Адрес"]
        for row in rows:
            output_table.add_row(row)
        print(output_table)

    elif result is None:
        if table_name == 1:
            cursor.execute("SELECT * FROM Readers;")
            rows = cursor.fetchall()
            output_table.field_names = ["Номер читательского билета"]
            output_table.title = "Читатели"
            for row in rows:
                output_table.add_row(row)
            print(output_table)

        if table_name == 2:
            cursor.execute("SELECT * FROM Persons ORDER BY id_reader_person ASC;")
            rows = cursor.fetchall()
            output_table.field_names = ["ID", "Номер читательского билета", "ФИО", "Пол", "Дата рождения", "Возраст",
                                        "Образование"]
            output_table.title = "Пользователи"
            for row in rows:
                output_table.add_row(row)
            print(output_table)

        if table_name == 3:
            cursor.execute("SELECT * FROM Addresses ORDER BY id_reader_address ASC;")
            rows = cursor.fetchall()
            output_table.field_names = ["Номер читательского билета", "Адрес"]
            output_table.title = "Адреса"
            for row in rows:
                output_table.add_row(row)
            print(output_table)


def sqlite_is_exists(sql_con, table_name, lib_num):
    cursor = sql_con.cursor()
    if table_name == 1:
        try:
            statement = cursor.execute(f"""
                SELECT EXISTS (SELECT * FROM Readers where id_reader = {lib_num});
            """)
            if statement.fetchone()[0]:
                return True
        except sqlite3.DatabaseError as err:
            print("Ошибка базы данных")


def sqlite_insert(sql_con, table_name, znash):
    cursor = sql_con.cursor()
    try:
        if table_name == 1:
            cursor.execute("""
                INSERT INTO Readers VALUES(?)
                    """, znash)
        elif table_name == 2:
            cursor.execute("""
                INSERT INTO Persons VALUES(NULL,?,?,?,?,?,?)
                    """, znash)

        elif table_name == 3:
            cursor.execute("""
                INSERT INTO Addresses VALUES(?,?)
                    """, znash)
        elif table_name == "all":
            readers = [znash[0]]
            persons = [znash[0], znash[1], znash[2],
                       znash[3], znash[4], znash[5]]
            addresses = [znash[0], znash[6]]

            cursor.execute("INSERT INTO Readers VALUES(?)", readers)
            cursor.execute("INSERT INTO Persons VALUES(NULL,?,?,?,?,?,?)", persons)
            cursor.execute("INSERT INTO Addresses VALUES(?,?)", addresses)
        else:
            print("Не найдено такой таблицы")
    except (sqlite3.IntegrityError, sqlite3.DatabaseError) as err:
        print("\tВы ввели неправильный номер читательского билета")
        print("Выберите номер билета из данного списка:")
        sqlite_select(sql_con, 1)
    sql_con.commit()


def sqlite_delete(sql_con, table_name, id):
    cursor = sql_con.cursor()
    if table_name == 1:
        cursor.execute(f"""
                DELETE FROM Readers WHERE id_reader = {id}
                """)
    elif table_name == 2:
        cursor.execute(f"""
                DELETE FROM Persons WHERE id_person = {id}
                    """)

    elif table_name == 3:
        cursor.execute(f"""
                DELETE FROM Addresses WHERE id_reader_address = {id}
                    """)
    else:
        print("Не найдено такой таблицы")
    sql_con.commit()
    cursor.close()


def sqlite_update(sql_con, table_name, znash, statement=None):
    cursor = sql_con.cursor()
    try:
        if table_name == 1:
            cursor.execute(f"""
                    UPDATE Readers SET id_reader = ? WHERE id_reader = ?
                        """, znash)
        elif table_name == 2:
            if statement == 1:
                cursor.execute("""
                         UPDATE Persons SET fio = ? WHERE id_reader_person = ?
                            """, znash)
            elif statement == 2:
                cursor.execute("""
                         UPDATE Persons SET gender = ? WHERE id_reader_person = ?
                            """, znash)
            elif statement == 3:
                cursor.execute("""
                         UPDATE Persons SET birthday = ? WHERE id_reader_person = ?
                            """, znash)
            elif statement == 4:
                cursor.execute("""
                         UPDATE Persons SET age = ? WHERE id_reader_person = ?
                            """, znash)
            elif statement == 5:
                cursor.execute("""
                         UPDATE Persons SET education = ? WHERE id_reader_person = ?
                            """, znash)
            elif statement == 6:
                cursor.execute("""
                            UPDATE Persons SET 
                            fio = ?,
                            gender = ?,
                            birthday = ?,
                            age = ?,
                            education = ?
                            WHERE id_reader_person = ?
                             """, znash)

        elif table_name == 3:
            cursor.execute("""
                    UPDATE Addresses SET address = ? WHERE id_reader_address = ?
                        """, znash)
        else:
            print("Не найдено такой таблицы")
    except (sqlite3.IntegrityError, sqlite3.DatabaseError) as err:
        print(err)
        print("\tВы ввели неправильный номер читательского билета")
        print("Выберите номер билета из данного списка:")
        sqlite_select(sql_con, 1)
    sql_con.commit()


def sqlite_output_group(sql_con, znash, statement=None):
    output_table = PrettyTable()
    cursor = sql_con.cursor()
    if statement == 1:
        sql_ex = """
                SELECT id_reader,
                fio, gender, birthday, age, education,
                address
                FROM Readers

                LEFT JOIN 
                Persons on Readers.id_reader = Persons.id_reader_person

                LEFT JOIN
                Addresses on Addresses.id_reader_address = Readers.id_reader
                WHERE age BETWEEN ? AND ? AND education = ?;
            """
    elif statement == 2:
        sql_ex = """
                SELECT id_reader,
                fio, gender, birthday, age, education,
                address
                FROM Readers

                LEFT JOIN 
                Persons on Readers.id_reader = Persons.id_reader_person

                LEFT JOIN
                Addresses on Addresses.id_reader_address = Readers.id_reader
                WHERE gender = ?
            """
    elif statement == 3:
        sql_ex = """
                SELECT id_reader,
                fio, gender, birthday, age, education,
                address
                FROM Readers

                LEFT JOIN 
                Persons on Readers.id_reader = Persons.id_reader_person

                LEFT JOIN
                Addresses on Addresses.id_reader_address = Readers.id_reader
                WHERE education = ? ORDER BY birthday;
        """
    elif statement == 4:
        sql_ex = """
                SELECT id_reader,
                fio, gender, birthday, age, education,
                address
                FROM Readers

                LEFT JOIN 
                Persons on Readers.id_reader = Persons.id_reader_person

                LEFT JOIN
                Addresses on Addresses.id_reader_address = Readers.id_reader
                WHERE id_reader BETWEEN ? AND ?;
        """
    elif statement == 5:
        sql_ex = """
                SELECT id_reader,
                fio, gender, birthday, age, education,
                address
                FROM Readers

                LEFT JOIN 
                Persons on Readers.id_reader = Persons.id_reader_person

                LEFT JOIN
                Addresses on Addresses.id_reader_address = Readers.id_reader
                WHERE fio LIKE ? ORDER BY age;
        """
    try:
        cursor.execute(sql_ex, znash)
    except sqlite3.ProgrammingError as err:
        print("Пожалуйста введите значения правильно!")
    else:
        rows = cursor.fetchall()
        output_table.field_names = ["Номер читательского билета", "ФИО",
                                    "Пол", "День рождения", "Возраст", "Образование",
                                    "Адрес"]
        for row in rows:
            output_table.add_row(row)
        print(output_table)


def sqlite_export_json(sql_con):
    def dict_factory(cursor, row):
        d = {}
        for j, i in enumerate(cursor.description):
            d[i[0]] = row[j]
        return d

    tables = ['Readers', 'Persons', 'Addresses']
    data = {}
    sql_con.row_factory = dict_factory
    cursor = sql_con.cursor()

    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        data[table] = rows

        with open("SQLite DataBase/LibraryReaders.json", 'w') as fp:
            json.dump(data, fp, indent=4)
