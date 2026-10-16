
import json

import pytest

from contact import Contact
from contact_file import ContactFile
from exceptions import FileNotExist


def test_save_and_load_contacts(tmp_path) -> None:
    file_path = tmp_path / "contacts.json"
    contact_file = ContactFile(file_path)

    contacts = [
        Contact("Иван", 123456789, "Работа"),
        Contact("Анна", 987654321, "Дом"),
    ]

    contact_file.save(contacts)
    loaded_contacts = contact_file.load()

    assert loaded_contacts == contacts


def test_load_missing_file(tmp_path) -> None:
    file_path = tmp_path / "missing.json"
    contact_file = ContactFile(file_path)

    with pytest.raises(FileNotExist):
        contact_file.load()


def test_saved_file_contains_json_lines(tmp_path) -> None:
    file_path = tmp_path / "contacts.json"
    contact_file = ContactFile(file_path)

    contacts = [
        Contact("Иван", 123456789, "Работа"),
        Contact("Анна", 987654321, "Дом"),
    ]

    contact_file.save(contacts)

    with file_path.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    assert len(lines) == 2
    assert json.loads(lines[0])["name"] == "Иван"
    assert json.loads(lines[1])["name"] == "Анна"
