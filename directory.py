
from pathlib import Path

from contact import Contact
from contact_file import ContactFile
from exceptions import PhoneAlreadyExists, PhoneNotExist


class Directory:
    """Управляет контактами телефонного справочника."""

    def __init__(self, file_path: Path) -> None:
        """Создаёт справочник и объект для работы с файлом."""
        self.contact_file = ContactFile(file_path)

    def get_all(self) -> list[Contact]:
        """Возвращает все контакты."""
        if not self.contact_file.file_path.exists():
            return []
        return self.contact_file.load()

    def phone_exists(self, phone: int) -> bool:
        """Проверяет, существует ли номер телефона."""
        for contact in self.get_all():
            if contact.phone == phone:
                return True
        return False

    def add_contact(self, contact: Contact) -> None:
        """Добавляет новый контакт."""
        contacts = self.get_all()

        for existing_contact in contacts:
            if existing_contact.phone == contact.phone:
                raise PhoneAlreadyExists("Такой номер уже существует")

        contacts.append(contact)
        self.contact_file.save(contacts)

    def find_contact(self, phone: int) -> Contact:
        """Находит контакт по номеру телефона."""
        for contact in self.get_all():
            if contact.phone == phone:
                return contact

        raise PhoneNotExist("Номер не найден")

    def edit_contact(
        self,
        phone: int,
        new_name: str,
        new_phone: int,
        new_comment: str,
    ) -> None:
        """Изменяет данные существующего контакта."""
        contacts = self.get_all()

        for index, contact in enumerate(contacts):
            if contact.phone == phone:
                if (
                    new_phone != phone
                    and any(
                        item.phone == new_phone
                        for item in contacts
                    )
                ):
                    raise PhoneAlreadyExists(
                        "Такой номер уже существует"
                    )

                contacts[index] = Contact(
                    name=new_name,
                    phone=new_phone,
                    comment=new_comment,
                )
                self.contact_file.save(contacts)
                return

        raise PhoneNotExist("Телефон не найден")

    def delete_contact(self, phone: int) -> None:
        """Удаляет контакт по номеру телефона."""
        contacts = self.get_all()

        for index, contact in enumerate(contacts):
            if contact.phone == phone:
                del contacts[index]
                self.contact_file.save(contacts)
                return

        raise PhoneNotExist("Телефон не найден")
