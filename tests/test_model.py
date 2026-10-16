
import json

import pytest

from contact import Contact
from exceptions import PhoneAlreadyExists, PhoneNotExist
from model import Model


@pytest.fixture
def model_and_file(tmp_path):
    """Создаёт модель и временный файл для тестирования."""
    path = tmp_path / "contacts.json"
    model = Model()

    # Направляем модель на временный файл вместо настоящего.
    model.directory.contact_file.file_path = path

    return model, path


def write_contacts(path, contacts):
    """Записывает контакты в файл в формате JSON Lines."""
    with open(path, "w", encoding="utf-8") as file:
        for contact in contacts:
            json.dump(contact, file, ensure_ascii=False)
            file.write("\n")


def test_get_all(model_and_file):
    """Проверяет загрузку всех контактов."""
    model, path = model_and_file
    write_contacts(
        path,
        [
            {"name": "Иван", "phone": 111, "comment": "Работа"},
            {"name": "Анна", "phone": 222, "comment": "Друг"},
        ],
    )

    assert model.get_all() == [
        Contact("Иван", 111, "Работа"),
        Contact("Анна", 222, "Друг"),
    ]


def test_get_all_without_file(model_and_file):
    """Проверяет получение пустого списка без файла."""
    model, path = model_and_file

    assert not path.exists()
    assert model.get_all() == []


def test_phone_exists(model_and_file):
    """Проверяет наличие и отсутствие номера."""
    model, path = model_and_file
    write_contacts(
        path,
        [{"name": "Иван", "phone": 111, "comment": "Работа"}],
    )

    assert model.phone_exists(111) is True
    assert model.phone_exists(999) is False


def test_add_contact(model_and_file):
    """Проверяет добавление нового контакта."""
    model, path = model_and_file
    write_contacts(
        path,
        [{"name": "Иван", "phone": 111, "comment": "Работа"}],
    )

    new_contact = Contact("Анна", 222, "Друг")
    model.add_contact(new_contact)

    assert model.get_all() == [
        Contact("Иван", 111, "Работа"),
        new_contact,
    ]


def test_add_contact_without_file(model_and_file):
    """Проверяет добавление контакта, если файла ещё нет."""
    model, path = model_and_file
    contact = Contact("Иван", 111, "Работа")

    model.add_contact(contact)

    assert path.exists()
    assert model.get_all() == [contact]


def test_add_duplicate_phone(model_and_file):
    """Проверяет запрет добавления повторного номера."""
    model, path = model_and_file
    write_contacts(
        path,
        [{"name": "Иван", "phone": 111, "comment": "Работа"}],
    )

    duplicate = Contact("Другой", 111, "Дом")

    with pytest.raises(PhoneAlreadyExists):
        model.add_contact(duplicate)


def test_find_contact(model_and_file):
    """Проверяет поиск существующего контакта."""
    model, path = model_and_file
    write_contacts(
        path,
        [{"name": "Иван", "phone": 111, "comment": "Работа"}],
    )

    assert model.find_contact(111) == Contact(
        "Иван", 111, "Работа"
    )


def test_find_missing_contact(model_and_file):
    """Проверяет ошибку при поиске отсутствующего номера."""
    model, path = model_and_file

    with pytest.raises(PhoneNotExist):
        model.find_contact(999)


def test_edit_contact(model_and_file):
    """Проверяет изменение данных контакта."""
    model, path = model_and_file
    write_contacts(
        path,
        [{"name": "Иван", "phone": 111, "comment": "Работа"}],
    )

    model.edit_contact(111, "Иван Петров", 333, "Дом")

    assert model.get_all() == [
        Contact("Иван Петров", 333, "Дом")
    ]


def test_edit_missing_contact(model_and_file):
    """Проверяет ошибку при редактировании отсутствующего контакта."""
    model, path = model_and_file

    with pytest.raises(PhoneNotExist):
        model.edit_contact(999, "Иван", 333, "Дом")


def test_edit_contact_duplicate_phone(model_and_file):
    """Проверяет запрет присвоения занятого номера."""
    model, path = model_and_file
    write_contacts(
        path,
        [
            {"name": "Иван", "phone": 111, "comment": "Работа"},
            {"name": "Пётр", "phone": 222, "comment": "Дом"},
        ],
    )

    with pytest.raises(PhoneAlreadyExists):
        model.edit_contact(111, "Иван", 222, "Работа")


def test_delete_contact(model_and_file):
    """Проверяет удаление контакта."""
    model, path = model_and_file
    write_contacts(
        path,
        [
            {"name": "Иван", "phone": 111, "comment": "Работа"},
            {"name": "Анна", "phone": 222, "comment": "Друг"},
        ],
    )

    model.delete_contact(111)

    assert model.get_all() == [
        Contact("Анна", 222, "Друг")
    ]


def test_delete_missing_contact(model_and_file):
    """Проверяет ошибку при удалении отсутствующего контакта."""
    model, path = model_and_file

    with pytest.raises(PhoneNotExist):
        model.delete_contact(999)


def test_delete_contact_without_file(model_and_file):
    """Проверяет удаление из ещё не созданного справочника."""
    model, path = model_and_file

    with pytest.raises(PhoneNotExist):
        model.delete_contact(999)
