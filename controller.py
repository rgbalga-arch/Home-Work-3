from model import Model
from contact import Contact
from view import View

from exceptions import FileNotExist, PhoneAlreadyExists, PhoneNotExist, WrongCommand


class Controller:
    """Управляет взаимодействием справочника и пользователя."""

    def __init__(self) -> None:
        self.model = Model()
        self.view = View()

    def new_reg(self) -> None:
        """Добавляет новый контакт."""
        phone = self.view.ask_phone()

        if self.model.phone_exists(phone):
            err = PhoneAlreadyExists("Такой номер уже существует")
            self.view.show_message(str(err))
            print(type(err).__name__)
            return

        contact = Contact(
            name=self.view.ask_name(),
            phone=phone,
            comment=self.view.ask_comment(),
        )

        try:
            self.model.add_contact(contact)
        except PhoneAlreadyExists as err:
            self.view.show_message(str(err))
            print(type(err).__name__)
            return

        self.view.show_message("Номер добавлен.")

    def see_all(self) -> None:
        """Показывает все контакты."""
        try:
            contacts = self.model.get_all()
            if not contacts:
                self.view.show_message("Справочник пуст.")
                return

            for contact in contacts:
                self.view.show_message(
                    f"Имя: {contact.name}, "
                    f"телефон: {contact.phone}, "
                    f"комментарий: {contact.comment}"
                )
        except FileNotExist as err:
            self.view.show_message(str(err))
            print(type(err).__name__)

    def find_one(self) -> None:
        """Находит контакт по номеру телефона."""
        phone = self.view.ask_phone()

        try:
            contact = self.model.find_contact(phone)
            self.view.show_message(
                f"Имя: {contact.name}, "
                f"телефон: {contact.phone}, "
                f"комментарий: {contact.comment}"
            )
        except PhoneNotExist as err:
            self.view.show_message(str(err))
            print(type(err).__name__)

    def edit_one(self) -> None:
        """Редактирует существующий контакт."""
        phone = self.view.ask_phone()

        try:
            self.model.find_contact(phone)
        except PhoneNotExist as err:
            self.view.show_message(str(err))
            print(type(err).__name__)
            return

        new_name = self.view.new_name()
        new_phone = self.view.new_phone()
        new_comment = self.view.new_comment()

        try:
            self.model.edit_contact(
                phone,
                new_name,
                new_phone,
                new_comment,
            )
            self.view.show_message("Контакт сохранён.")
        except (PhoneAlreadyExists, PhoneNotExist) as err:
            self.view.show_message(str(err))
            print(type(err).__name__)

    def delete_one(self) -> None:
        """Удаляет контакт по номеру телефона."""
        phone = self.view.ask_phone()

        try:
            self.model.delete_contact(phone)
            self.view.show_message("Контакт удалён.")
        except PhoneNotExist as err:
            self.view.show_message(str(err))
            print(type(err).__name__)

    def start(self) -> None:
        """Запускает главное меню приложения."""
        while True:
            action = self.view.menu()

            try:
                if action == "1":
                    self.new_reg()
                elif action == "2":
                    self.see_all()
                elif action == "3":
                    self.find_one()
                elif action == "4":
                    self.edit_one()
                elif action == "5":
                    self.delete_one()
                else:
                    raise WrongCommand("Неверная команда")
            except WrongCommand as err:
                self.view.show_message(str(err))
                print(type(err).__name__)
