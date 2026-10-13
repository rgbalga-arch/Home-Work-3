import json
from pathlib import Path


contacts_path = Path("contacts.json")
"""путь к файлу"""


class AppError(Exception):
    """базовое исключение"""
    pass


class FileNotExist(AppError):
    """ошибка: файла не существует"""
    pass


class UserError(AppError):
    """базорвая ошибка юзера"""
    pass


class PhoneNotExist(UserError):
    """ошибка: такого телефона нет"""
    pass


class DelContact:
    def delete(self) -> None:
        data_search: list[dict] = []
        """создаем пустой список"""

        with open("contacts.json", "r", encoding="UTF-8") as contacts_file:
            """открываем файл для чтения"""
            for line in contacts_file:
                """читаем построчно"""
                data_search.append(json.loads(line))
                """преобразуем JSON строку в словарь Python"""

        while True:
            key: str = input("Введите теелфон для поиска: ")
            """запрашиваем телефон у пользователя"""

            found: bool = False
            """показывает был ли найден контакт"""

            try:
                for contact in data_search:
                    """перебираем все контакты"""
                    if key == str(contact["phone"]):
                        """проверяем есть ли введеный номер в номере проверяемой строки"""
                        print(contact)
                        """выводим найденный контакт"""

                        found = True
                        """запоминаем, что контакт был найден"""

                        data_search.remove(contact)
                        """удаляем найденный контакт"""

                        with open("contacts.json", "w", encoding="UTF-8") as contacts_file:
                            """открываем файл в режиме записи"""

                            for contact in data_search:
                                json.dump(contact, contacts_file, ensure_ascii=False)
                                contacts_file.write("\n")
                                """записываем оставшиеся контакты обратно в файл и переходим на новую строку"""

                        print(data_search)
                        """выводим обновленный список"""
                        break


                if not found:
                    raise PhoneNotExist("телефон не существует")
                break

            except PhoneNotExist as err:
                print(err)
                print(type(err).__name__)
                break