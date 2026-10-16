
from pathlib import Path

from contact import Contact
from directory import Directory


class Model:
    """Предоставляет контроллеру доступ к данным справочника."""

    def __init__(self) -> None:
        """Создаёт объект для работы со справочником."""
        self.directory = Directory(Path("contacts.json"))

    def get_all(self) -> list[Contact]:
        """Возвращает все контакты."""
        return self.directory.get_all()

    def phone_exists(self, phone: int) -> bool:
        """Проверяет, существует ли номер телефона."""
        return self.directory.phone_exists(phone)

    def add_contact(self, contact: Contact) -> None:
        """Добавляет контакт."""
        self.directory.add_contact(contact)

    def find_contact(self, phone: int) -> Contact:
        """Находит контакт по номеру телефона."""
        return self.directory.find_contact(phone)

    def edit_contact(
        self,
        phone: int,
        new_name: str,
        new_phone: int,
        new_comment: str,
    ) -> None:
        """Редактирует контакт."""
        self.directory.edit_contact(
            phone,
            new_name,
            new_phone,
            new_comment,
        )

    def delete_contact(self, phone: int) -> None:
        """Удаляет контакт."""
        self.directory.delete_contact(phone)
