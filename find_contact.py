from pathlib import Path

contacts_path = Path("contacts.json")
"""путь к контактам"""
import json

class AppError(Exception):
    """базовый класс ошибок"""
    pass

class UserError(AppError):
    """класс ошибок, связанный с пользователем"""
    pass

class PhoneNotExist(UserError):
    """ошибка: такого номера нет"""
    pass

class ContFinder:
    def search_all(self) -> None:

        while True:
            data_search: list[dict] = []
            """создаем пустой список"""
            with open(contacts_path, "r", encoding="UTF-8") as contacts_file:
                """открываем файл с контактами для чтения"""
                for line in contacts_file:
                    """читаем построчно"""
                    data_search.append(json.loads(line))
                    """преобразуем JSON в словарь Python"""

            try:
                key: str = input("Введите теелфон для поиска: ").lower()
                """запрашиваем номер для поиска"""

                found: bool = False

                for contact in data_search:
                    """перебираем все контакты"""
                    if key in str(contact["phone"]).lower():
                        """преобразуем телефон в строку и смотрим есть ли такое значение"""
                        print(contact)
                        """выводим найденный контакт"""
                        found = True
                        """запоминаем, что контакт был найден"""

                if not found:
                    raise PhoneNotExist("Файл не найден")
                """если контакт не найден, выводим текст и собственное исключение"""
            except PhoneNotExist as err:
                print(err)
                print(type(err).__name__)