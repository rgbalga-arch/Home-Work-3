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


class NewContact:
    def new_reg(self):
        data_cont: list[dict] = []
        """Создаём список для хранения существующих контактов."""

        if contacts_path.exists():
            """Проверяем, существует ли файл с контактами"""
            with open(contacts_path, "r", encoding="UTF-8") as contacts_file:
                for line in contacts_file:
                    """Читаем каждый контакт из отдельной строки JSON"""
                    data_cont.append(json.loads(line))

        name: str = input("напишите имя ")
        """Запрашиваем имя нового контакта"""

        while True:
            """Повторяем ввод, пока пользователь не введёт число"""
            try:
                phone = int(input("Введите номер телефона: "))
                break
            except ValueError:
                print("Введите только цифры.")

        for contact in data_cont:
            if phone == contact["phone"]:
                """Проверяем, нет ли такого номера среди существующих контактов"""
                print("Такой номер уже существует.")
                return
                """если номер есть, то останавливаем new_reg"""

        comment: str = input("Напишите комментарий ")
        """Запрашиваем комментарий к контакту"""

        phone_list = {"name": name, "phone": phone, "comment": comment}
        """Создаём словарь с данными нового контакта"""

        with open("contacts.json", "a", encoding="UTF-8") as contacts_file:
            json.dump(phone_list, contacts_file, ensure_ascii=False)
            """Открываем файл в режиме добавления нового контакта и добавляем строку"""
            contacts_file.write("\n")
            print("номер добавлен")
