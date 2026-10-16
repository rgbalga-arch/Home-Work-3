
import pytest

from contact import Contact
from directory import Directory
from exceptions import PhoneAlreadyExists, PhoneNotExist


def test_add_and_find_contact(tmp_path) -> None:
    directory = Directory(tmp_path / "contacts.json")
    contact = Contact("Иван", 123456789, "Работа")

    directory.add_contact(contact)

    assert directory.find_contact(123456789) == contact


def test_add_duplicate_phone(tmp_path) -> None:
    directory = Directory(tmp_path / "contacts.json")
    contact = Contact("Иван", 123456789, "Работа")

    directory.add_contact(contact)

    with pytest.raises(PhoneAlreadyExists):
        directory.add_contact(
            Contact("Анна", 123456789, "Дом")
        )


def test_find_missing_contact(tmp_path) -> None:
    directory = Directory(tmp_path / "contacts.json")

    with pytest.raises(PhoneNotExist):
        directory.find_contact(123456789)


def test_edit_contact(tmp_path) -> None:
    directory = Directory(tmp_path / "contacts.json")
    directory.add_contact(
        Contact("Иван", 123456789, "Работа")
    )

    directory.edit_contact(
        123456789,
        "Иван Иванов",
        987654321,
        "Дом",
    )

    assert directory.find_contact(987654321) == Contact(
        "Иван Иванов",
        987654321,
        "Дом",
    )


def test_delete_contact(tmp_path) -> None:
    directory = Directory(tmp_path / "contacts.json")
    directory.add_contact(
        Contact("Иван", 123456789, "Работа")
    )

    directory.delete_contact(123456789)

    assert directory.get_all() == []


def test_delete_missing_contact(tmp_path) -> None:
    directory = Directory(tmp_path / "contacts.json")

    with pytest.raises(PhoneNotExist):
        directory.delete_contact(123456789)
