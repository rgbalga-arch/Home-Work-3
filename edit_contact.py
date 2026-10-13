import json
from pathlib import Path


contacts_path = Path("contacts.json")
"""Путь к файлу с контактами"""


class AppError(Exception):
    """Базовое исключение приложения"""
    pass


class FileNotExist(AppError):
    """Ошибка: файл с контактами не существует"""
    pass


class UserError(AppError):
    """Базовое исключение пользователя"""
    pass


class PhoneNotExist(UserError):
    """Ошибка: телефон не найден"""
    pass


class ContEditor:
    def edit_contacts(self) -> None:
        data_search: list[dict] = []
        """Создаём пустой список для хранения контактов"""

        with open(contacts_path, "r", encoding="UTF-8") as contacts_file:
            """Открываем файл с контактами для чтения"""
            for line in contacts_file:
                """Читаем файл построчно"""
                data_search.append(json.loads(line))
                """Преобразуем JSON-строку в словарь Python"""

        while True:
            key: str = input("Введите телефон для поиска: ")
            """Запрашиваем у пользователя телефон для поиска"""

            found: bool = False
            """Флаг показывает, найден ли контакт"""

            try:
                for contact in data_search:
                    """Перебираем все контакты"""
                    if key == str(contact["phone"]):
                        """Проверяем, содержится ли введённый номер в номере телефона текущего контакта"""
                        new_name: str = input("Введите новое имя: ")
                        new_phone: str = input("Введите новый телефон: ")
                        new_comment: str = input("Введите новый комментарий: ")
                        """Запрашиваем новые данные контакта"""
                        contact["name"] = new_name
                        contact["phone"] = int(new_phone)
                        contact["comment"] = new_comment
                        """Обновляем данные контакта"""

                        found = True
                        """Запоминаем, что контакт найден и ниже прекращаем поиск после первого совпадения"""
                        break

                if found:
                    with open(contacts_path, "w", encoding="UTF-8") as contacts_file:
                        """Открываем файл для перезаписи"""
                        for contact in data_search:
                            json.dump(contact, contacts_file, ensure_ascii=False)
                            contacts_file.write("\n")
                            """Записываем все контакты обратно в файл"""

                    print("контакт сохранен")
                    """Сообщаем пользователю об успешном сохранении"""

                if not found:

                    raise PhoneNotExist("телефон не найден")
                """если контакт не найден - выводим сообщение и собственную ошибку"""
            except PhoneNotExist as err:
                print(err)
                print(type(err).__name__)
                break

