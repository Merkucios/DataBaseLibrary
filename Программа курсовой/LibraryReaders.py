# Класс сведений об читателях
class LibraryReaders:
    def __init__(self):
        # Номер читательского билета
        self.__lib_card_num = None
        # Фамилия и инициалы читателя
        self.__surname_np = None
        # Дата рождения читателя
        self.__birthday_date = None
        # Возраст читателя
        self.__age = None
        # Пол читателя
        self.__gender = None
        # Адрес читателя
        self.__address = None
        # Уровень образования
        self.__education = None

    @property
    def lib_card_num(self):
        return self.__lib_card_num

    @lib_card_num.setter
    def lib_card_num(self, value):
        while True:
            try:
                k = int(input("Введите номер читательского билета\t"))
                if k < 0:
                    raise ValueError
            except (TypeError, ValueError) as err:
                print("Напишите ваш номер цифрами")
            else:
                self.__lib_card_num = k
                break

    @property
    def surname_np(self):
        return self.__surname_np

    @surname_np.setter
    def surname_np(self, value):
        while True:
            try:
                k = input("Введите фамилию, имя и отчество\t")
            except (TypeError, ValueError) as err:
                print("Введите допустимую запись ФИО")
            else:
                try:
                    surname, name, patronymic = k.split()
                    if surname.isdigit() or name.isdigit() or patronymic.isdigit():
                        print("Введите правильное ФИО\n\tНапример: Бузова Ольга Петровна")
                    else:
                        lower = surname.lower()
                        self.__surname_np = f"{lower.replace(lower[0], lower[0].upper(), 1)} {name[0].upper()}.{patronymic[0].upper()}.".format(
                            **vars())
                        break
                except (TypeError, ValueError) as err:
                    print("Введите правильное ФИО\n\tНапример: Бузова Ольга Петровна")

    @property
    def birthday_date(self):
        return self.__birthday_date

    @birthday_date.setter
    def birthday_date(self, value):
        while True:
            try:
                k = int(input("Введите дату рождения (только год)\t"))
            except (TypeError, ValueError) as err:
                print("Введите дату рождения цифрами")
            else:
                if 1910 < k <= 2022:
                    self.__birthday_date = k
                    break
                else:
                    print("Вы ввели недопустимую дату рождения")

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        while True:
            try:
                k = int(input("Введите возраст\t"))
            except (TypeError, ValueError) as err:
                print("Введите возраст цифрами")
            else:
                if 5 < k <= 115:
                    self.__age = k
                    break
                else:
                    print("Вы ввели недопустимый возраст")

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, value):
        print("Введите пол:\n"
              "М - Мужской\n"
              "Ж - Женский")
        while True:
            k = input("Ваш пол\t").upper()
            if k == "Ж" or k == "М":
                self.__gender = k
                break
            else:
                print("Вы неправильно написали пол")

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        street = ["Ул. Ленина", "Ул. Истомина", "Ул. Лейтенанта Орлова", "Ул. Дикопольцева",
                  "Ул. Мухина", "Ул. Гамарника"]
        while True:
            print("Введите адрес проживания читателя\n"
                  "1 - Ленина\n"
                  "2 - Истомина\n"
                  "3 - Лейтенанта Орлова\n"
                  "4 - Дикопольцева\n"
                  "5 - Мухина\n"
                  "6 - Гамарника")
            try:
                k = int(input("Адрес -\t"))
                if k > 6:
                    raise ValueError
            except (TypeError, ValueError) as err:
                print("Введите значение адреса от 1 до 6")
            else:
                try:
                    address_ha = input("Введите номер дома и квартиры\t")
                    home, apartment = address_ha.split()
                    try:
                        if home[0].isdigit and len(home) <= 3:
                            if apartment[0].isdigit and len(apartment) <= 3:
                                self.__address = f"{street[k - 1]}, д.{home}, кв.{apartment}".format(**vars())
                                break
                            else:
                                print("Вы ввели недопустимое значение номера кватиры")
                        else:
                            print("Вы ввели недопустимое значение номера дома")
                    except (TypeError, ValueError) as err:
                        print("Введите номер дома и квартиры цифрами\n\tДом - 23\n\tКвартира - 13")
                except (TypeError, ValueError) as err:
                    print("Введите правильный адрес\n\tНапример: Ленина 73 14")

    @property
    def education(self):
        return self.__education

    @education.setter
    def education(self, value):
        educt = ["Высшее", "Среднее", "Школьное"]
        print("Введите уровень вашего образования:\n"
              "1 - Высшее\n"
              "2 - Среднее\n"
              "3 - Школьное")
        while True:
            try:
                k = int(input("Введите уровень образования\t"))
            except (TypeError, ValueError, IndexError) as err:
                print("Введите значение от одного до трёх")
            else:
                if 1 <= k <= 3:
                    self.__education = educt[k - 1]
                    break
                else:
                    print("Вы неправильно ввели уровень образования")
