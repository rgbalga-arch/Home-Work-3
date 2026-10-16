
import json
from pathlib import Path

from contact import Contact
from exceptions import FileNotExist


class ContactFile:
    """Отвечает за чтение и запись контактов в JSON Lines."""

    def __init__(self, file_path: Path) -> None:
        """Сохраняет путь к файлу справочника."""
        self.file_path = file_path

    def load(self) -> list[Contact]:
        """Загружает контакты из файла."""
        if not self.file_path.exists():
            raise FileNotExist("Файл не найден")

        contacts = []

        with self.file_path.open("r", encoding="utf-8") as file:
            for line in file:
                data = json.loads(line)
                contact = Contact(**data)
                contacts.append(contact)

        return contacts

    def save(self, contacts: list[Contact]) -> None:
        """Сохраняет контакты в файл."""
        with self.file_path.open("w", encoding="utf-8") as file:
            for contact in contacts:
                json.dump(
                    {
                        "name": contact.name,
                        "phone": contact.phone,
                        "comment": contact.comment,
                    },
                    file,
                    ensure_ascii=False,
                )
                file.write("\n")
