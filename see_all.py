import json
from pathlib import Path

#путь к файлу с контактами
contacts_path = Path("contacts.json")


class AppError(Exception):
    """базовый класс ошибок приложения"""
    pass


class FileNotExist(AppError):
    """ошибка: файл не существует"""
    pass


class SeeAllList:
    def read_contacts(self) -> None:
        """читает и выводит все контакты из файла"""
        while True:
            try:
                if not contacts_path.exists():
                    raise FileNotExist("файл не найден")
                    """если фала нет, то пишем ошибку и показываем исключение"""

                with open(contacts_path, "r", encoding="UTF-8") as contacts_file:
                        """открываем файл в режиме чтения"""
                        data_cont = contacts_file.readlines()
                        """читаем все строки"""

                        for line in data_cont:
                            """смотрим каждую строку"""
                            contact = json.loads(line)
                            print(json.dumps(contact, indent=4))
                            """приводим в удобный формат"""

                break

            except FileNotExist as err:
                print(err)
                print(type(err).__name__)
                break


