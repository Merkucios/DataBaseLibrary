import time

import DefOfSQLite as DefSQL
from LibraryReaders import LibraryReaders as LibReader


def function_input():
    print("Введите функцию для работы с таблицей\n"
          "1 - Добавить запись\n"
          "2 - Удалить запись\n"
          "3 - Обновить запись\n"
          "4 - Вывести списки\n"
          "5 - Экспортировать БД в JSON\n"
          "6 - Помощь\n"
          "7 - Выход из программы")
    try:
        function = int(input())
    except (TypeError, ValueError):
        print("Вы ввели недопустимые значения номера функции")
        return function_input()
    else:
        if function < 1 or function > 7:
            print("Такой функции не существует")
            return function_input()
        else:
            return function


def table_input():
    print("Введите таблицу для работы\n"
          "1 - Читатели\n"
          "2 - Пользователи\n"
          "3 - Адреса")
    try:
        table_name = int(input())
    except (TypeError, ValueError):
        print("Вы ввели недопустимое значение номера таблицы")
        return table_input()
    else:
        if table_name < 1 or table_name > 4:
            print("Такой таблицы не существует")
            return table_input()
        else:
            return table_name


def insert_data(iterat, table_name, _readers):
    if table_name == 1:
        return [_readers[iterat].lib_card_num]
    if table_name == 2:
        return [_readers[iterat].lib_card_num, _readers[iterat].surname_np, _readers[iterat].gender,
                _readers[iterat].birthday_date, _readers[iterat].age, _readers[iterat].education]
    if table_name == 3:
        return [_readers[iterat].lib_card_num, _readers[iterat].address]
    if table_name == "all":
        return [_readers[iterat].lib_card_num, _readers[iterat].surname_np,
                _readers[iterat].gender, _readers[iterat].birthday_date,
                _readers[iterat].age, _readers[iterat].education,
                _readers[iterat].address]


_readers = [LibReader()]
print("Здравствуйте - это программма для работы со списками Библиотеки 📚")
sql_con = DefSQL.sqlite_connect()
DefSQL.sqlite_table(sql_con)

while True:
    DefSQL.sqlite_select(sql_con, 1, True)
    func = function_input()
    if 4 <= func <= 7:
        pass
    else:
        if func == 1:
            try:
                insert_all = int(input("Добавить запись полностью?\n1 -\tДа\n2 -\tНет\n"))
                if insert_all == 1 or insert_all == 2:
                    pass
                else:
                    raise ValueError
            except (TypeError, ValueError) as err:
                print("Введите знаение от 1 до 2")
            else:
                table_name = table_input()
        else:
            table_name = table_input()

    if func == 1:
        while True:
            i = 0
            if insert_all == 1:
                DefSQL.sqlite_select(sql_con, 1, True)
                _readers[i].lib_card_num = ()
                is_exists = DefSQL.sqlite_is_exists(sql_con, 1, _readers[i].lib_card_num)
                if is_exists:
                    print("Выберите другой читательский билет")
                elif not is_exists:
                    _readers[i].surname_np = ()
                    _readers[i].gender = ()
                    _readers[i].birthday_date = ()
                    _readers[i].age = ()
                    _readers[i].education = ()
                    _readers[i].address = ()
                    DefSQL.sqlite_insert(sql_con, "all", insert_data(i, "all", _readers))
                    DefSQL.sqlite_select(sql_con, table_name, True)
            elif insert_all == 2:
                DefSQL.sqlite_select(sql_con, table_name)
                if table_name == 1:
                    _readers[i].lib_card_num = ()
                elif table_name == 2:
                    _readers[i].lib_card_num = ()
                    is_exists = DefSQL.sqlite_is_exists(sql_con, 1, _readers[i].lib_card_num)
                    if is_exists:
                        _readers[i].surname_np = ()
                        _readers[i].gender = ()
                        _readers[i].birthday_date = ()
                        _readers[i].age = ()
                        _readers[i].education = ()
                    elif not is_exists:
                        print("Выберите другой читательский билет")
                    else:
                        print("Не существует такого читательского билета")
                elif table_name == 3:
                    _readers[i].lib_card_num = ()
                    is_exists = DefSQL.sqlite_is_exists(sql_con, 1, _readers[i].lib_card_num)
                    if is_exists:
                        _readers[i].address = ()
                    if not is_exists:
                        print("Выберите другой читательский билет")
                DefSQL.sqlite_insert(sql_con, table_name, insert_data(i, table_name, _readers))
                DefSQL.sqlite_select(sql_con, table_name)
            try:
                statement = int(
                    input("Введите:\n\t1 - Чтобы продолжить работу\n\t2 - Чтобы прекратить ввод данных\n"))
            except (TypeError, ValueError) as err:
                print("Введите целое число")
            else:
                if statement == 1:
                    pass
                elif statement == 2:
                    break

    if func == 2:
        while True:
            DefSQL.sqlite_select(sql_con, table_name)
            try:
                id = int(input("Введите ID читателя\t"))
            except (TypeError, ValueError) as err:
                print("Введите целое число")
            else:
                is_exists = DefSQL.sqlite_is_exists(sql_con, 1, id)
                if is_exists:
                    DefSQL.sqlite_delete(sql_con, 1, id)
                    print(f"Запись {id} успешно удалена!")
                elif not is_exists:
                    print("Не существует такого билета!")
                try:
                    statement = int(input(
                        "\tЧтобы продолжить удаление записей введите -\t1\n\tЧтобы завершить работу введите -\t2\n"))
                except (TypeError, ValueError) as err:
                    print("Введите 1 или 2")
                else:
                    if statement == 1:
                        pass
                    if statement == 2:
                        break
    if func == 3:
        new_value = LibReader()
        i = 0
        while True:
            DefSQL.sqlite_select(sql_con, table_name)
            print("* Номер для изменения *")
            _readers[i].lib_card_num = ()
            if table_name == 1:
                print("* Новый номер билета *")
                new_value.lib_card_num = ()
                new = [new_value.lib_card_num,
                       _readers[i].lib_card_num]
                DefSQL.sqlite_update(sql_con, table_name, new)
                print("Данные успешно обновлены!")

            elif table_name == 2:
                print("Какое поле вы хотите изменить?\n"
                      "1 - ФИО\n"
                      "2 - Пол\n"
                      "3 - Дата рождения\n"
                      "4 - Возраст\n"
                      "5 - Образование\n"
                      "6 - Обновить запись в таблице полностью")
                try:
                    statement = int(input("Введите нужное поле -\t"))
                    if statement > 6:
                        raise ValueError
                except (TypeError, ValueError) as err:
                    print("\tВведите правильное поле для изменения")
                else:
                    print("* Новые значения полей *")
                    if statement == 1:
                        new_value.surname_np = ()
                        new = [new_value.surname_np, _readers[i].lib_card_num]
                        DefSQL.sqlite_update(sql_con, table_name, new, statement)
                    elif statement == 2:
                        new_value.gender = ()
                        new = [new_value.gender, _readers[i].lib_card_num]
                        DefSQL.sqlite_update(sql_con, table_name, new, statement)
                    elif statement == 3:
                        new_value.birthday_date = ()
                        new = [new_value.birthday_date, _readers[i].lib_card_num]
                        DefSQL.sqlite_update(sql_con, table_name, new, statement)
                    elif statement == 4:
                        new_value.age = ()
                        new = [new_value.age, _readers[i].lib_card_num]
                        DefSQL.sqlite_update(sql_con, table_name, new, statement)
                    elif statement == 5:
                        new_value.education = ()
                        new = [new_value.education, _readers[i].lib_card_num]
                        DefSQL.sqlite_update(sql_con, table_name, new, statement)
                    elif statement == 6:
                        new_value.surname_np = ()
                        new_value.gender = ()
                        new_value.birthday_date = ()
                        new_value.age = ()
                        new_value.education = ()
                        new = [new_value.surname_np, new_value.gender,
                               new_value.birthday_date, new_value.age,
                               new_value.education,
                               _readers[i].lib_card_num]
                        DefSQL.sqlite_update(sql_con, table_name, new, statement)

            elif table_name == 3:
                print("* Новый адрес *")
                new_value.address = ()
                new = [new_value.address,
                       _readers[i].lib_card_num]
                DefSQL.sqlite_update(sql_con, table_name, new)
                print("Данные успешно обновлены!")

            DefSQL.sqlite_select(sql_con, table_name)

            try:
                statement = int(input(
                    "\tЧтобы продолжить обновление записей введите -\t1\n\tЧтобы завершить работу введите -\t2\n"))
            except (TypeError, ValueError) as err:
                print("Введите 1 или 2")
            else:
                if statement == 1:
                    pass
                if statement == 2:
                    break

    if func == 4:
        output_value = LibReader()
        output_list = []
        while True:
            print("Какой список вам требуется вывести?\n"
                  "1 - По диапазону возраста и образованию\n"
                  "2 - По полу\n"
                  "3 - По образованию, отсортированный по году рождения читателя\n"
                  "4 - По диапазону номера читательского билета\n"
                  "5 - По букве фамилии, отсортированной по возрасту")
            try:
                statement = int(input("Введите нужный список -\t"))
                if statement > 5:
                    raise ValueError
            except (TypeError, ValueError) as err:
                print("\tВведите список в значениях от 1 до 5")
            else:
                if statement == 1:
                    try:
                        start_between = int(input("Введите от какого возраста вывести список -\t"))
                    except (TypeError, ValueError) as err:
                        print("Введите пожалуйста число")
                    else:
                        try:
                            end_between = int(input("Введите до какого возраста вывести список -\t"))
                        except (TypeError, ValueError) as err:
                            print("Введите пожалуйста число")
                        else:
                            output_value.education = ()
                            output_list = [start_between, end_between,
                                           output_value.education]

                elif statement == 2:
                    output_value.gender = ()
                    output_list = [output_value.gender]
                elif statement == 3:
                    output_value.education = ()
                    output_list = [output_value.education]
                elif statement == 4:
                    try:
                        start_between = int(input("Введите от какого билета вывести список -\t"))
                    except (TypeError, ValueError) as err:
                        print("Введите пожалуйста число")
                    else:
                        try:
                            end_between = int(input("Введите до какого билета вывести список -\t"))
                        except (TypeError, ValueError) as err:
                            print("Введите пожалуйста число")
                        else:
                            output_list = [start_between, end_between]
                elif statement == 5:
                    letter = input("Введите букву фамилии для поиска -\t")
                    if letter.isdigit():
                        print("Введите пожалуйста букву")
                    else:
                        output_list = [f"{letter.upper()}%"]
                else:
                    print("Введите другое условие")
                DefSQL.sqlite_output_group(sql_con, output_list, statement)

            try:
                statement = int(input(
                    "\tЧтобы продолжить вывод списков введите -\t1\n\tЧтобы завершить работу введите -\t2\n"))
            except (TypeError, ValueError) as err:
                print("Введите 1 или 2")
            else:
                if statement == 1:
                    pass
                if statement == 2:
                    break
    if func == 5:
        DefSQL.sqlite_export_json(sql_con)
        print("База данных успешно экспортирована в JSON")
        sql_con = DefSQL.sqlite_connect()

    if func == 6:
        file = r"D:\Курсовая работа\Программа курсовой\Manual\Помощь.txt"
        try:
            manual = open(file, "r", encoding='utf-8')
        except FileNotFoundError:
            print("Невозможно найти файл \"Помощь\"")
        else:
            for line in manual:
                print(line, end="")
        finally:
            manual.close()
        print()
        print()
    if func == 7:
        DefSQL.sqlite_disconnect(sql_con)
        print("Спасибо за работу в программе!")
        time.sleep(3)
        break

    print("Чтобы продолжить работу введите -\t5\n"
          "Чтобы выйти из программы введите -\t6")
    try:
        exit_prog = int(input())
    except (TypeError, ValueError) as err:
        print("Введите:\n\t"
              "5 - Для продолжения работы\n\t"
              "6 - Для выхода из программы ")
    else:
        if exit_prog == 6:
            DefSQL.sqlite_disconnect(sql_con)
            print("Спасибо за работу в программе!")
            time.sleep(3)
            break
        elif exit_prog == 5:
            continue
