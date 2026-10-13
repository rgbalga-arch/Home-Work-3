import json
from pathlib import Path

contacts_path = Path("contacts.json")

class AppError(Exception):
    """Базовая ошибка приложения."""
    pass


class UserError(AppError):
    """Базовая ошибка, связанная с пользователем."""
    pass


class PhoneAlreadyExists(UserError):
    """Ошибка: такой номер телефона уже существует."""
    pass


class OnlyNumbersError(AppError):
    """Ошибка: номер телефона должен содержать только цифры."""
    pass


class FileNotExist(AppError):
    """ошибка: файл не существует"""
    pass


class PhoneNotExist(UserError):
    """Ошибка: телефон не найден"""
    pass


class WrongCommand(AppError):
    pass


class Model:
    def new_reg(self) -> list[dict]:
        data_cont: list[dict] = []
        """Создаём список для хранения существующих контактов."""

        if contacts_path.exists():
            """Проверяем, существует ли файл с контактами"""
            with open(contacts_path, "r", encoding="UTF-8") as contacts_file:
                for line in contacts_file:
                    """Читаем каждый контакт из отдельной строки JSON"""
                    data_cont.append(json.loads(line))
        return data_cont

    # def phone_exists(self, phone: int) -> bool:
    #     """Проверяет, существует ли такой номер."""
    #     data_cont = self.new_reg()
    #
    #     for contact in data_cont:
    #         if phone == contact["phone"]:
    #             return True
    #
    #     return False

    def phone_exists(self, phone: int) -> bool:
        """Проверяет, существует ли контакт с таким номером."""
        with open(contacts_path, "r", encoding="UTF-8") as contacts_file:
            for line in contacts_file:
                contact = json.loads(line)

                if contact["phone"] == phone:
                    return True

        return False

    def add_contact(self, phone_list: dict) -> None:
        """Добавляет контакт в файл."""
        if self.phone_exists(phone_list["phone"]):
            raise PhoneAlreadyExists("Такой номер уже существует")

        with open(contacts_path, "a", encoding="UTF-8") as contacts_file:
            json.dump(phone_list, contacts_file, ensure_ascii=False)
            contacts_file.write("\n")

    def read_contacts(self) -> list[dict]:
        if not contacts_path.exists():
            raise FileNotExist("файл не найден")

        with open(contacts_path, "r", encoding="UTF-8") as contacts_file:
            """открываем файл в режиме чтения"""
            data_cont = contacts_file.readlines()
            """читаем все строки"""
            for line in data_cont:
                """смотрим каждую строку"""
                contact = json.loads(line)
                print(json.dumps(contact, indent=4))
                """приводим в удобный формат"""

    def find_contact(self, phone: int) -> dict:
        with open(contacts_path, "r", encoding="UTF-8") as contacts_file:
            """открываем файл в режиме чтения"""
            for line in contacts_file:
                """смотрим каждую строку"""
                contact = json.loads(line)

                if contact["phone"] == phone:
                    return contact
        raise PhoneNotExist("Номер не найден")

    def edit_contact(self,phone: int,new_name: str,new_phone: int,new_comment: str) -> None:
        """Изменяет контакт и сохраняет изменения в файл."""
        data_search: list[dict] = []

        with open(contacts_path, "r", encoding="UTF-8") as contacts_file:
            for line in contacts_file:
                data_search.append(json.loads(line))
            """Читаем все контакты из файла."""

        for contact in data_search:
            if phone == contact["phone"]:
                """Ищем контакт по старому номеру"""
                contact["name"] = new_name
                contact["phone"] = new_phone
                contact["comment"] = new_comment
                break
        else:
            raise PhoneNotExist("Телефон не найден")

        with open(contacts_path, "w", encoding="UTF-8") as contacts_file:
            for contact in data_search:
                json.dump(contact, contacts_file, ensure_ascii=False)
                contacts_file.write("\n")
                """Сохраняем все контакты обратно в файл"""

    def delete_contact(self, phone: int) -> None:
        """Изменяет контакт и сохраняет изменения в файл."""
        data_search: list[dict] = []

        with open(contacts_path, "r", encoding="UTF-8") as contacts_file:
            for line in contacts_file:
                data_search.append(json.loads(line))
            """Читаем все контакты из файла."""

        for contact in data_search:
            if phone == contact["phone"]:
                """Ищем контакт по старому номеру"""
                data_search.remove(contact)
                break
        else:
            raise PhoneNotExist("Телефон не найден")

        with open(contacts_path, "w", encoding="UTF-8") as contacts_file:
            for contact in data_search:
                json.dump(contact, contacts_file, ensure_ascii=False)
                contacts_file.write("\n")
                """Сохраняем все контакты обратно в файл"""