from pathlib import Path
import json
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
        if contacts_path.exists():
            """проверяем, есть ли такой файл"""
            with open(contacts_path, "r", encoding="UTF-8") as contacts_file:
                """открываем файл в режиме чтения"""
                data_cont = contacts_file.readlines()
                """читаем все строки"""

                for line in data_cont:
                    """смотрим каждую строку"""
                    contact = json.loads(line)
                    print(json.dumps(contact, indent=4))
                    """приводим в удобный формат"""

        else:
            print("файл не существует")
            raise FileNotExist()
            """если фала нет, то пишем ошибку и показываем исключение"""


