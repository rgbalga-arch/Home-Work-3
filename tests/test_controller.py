
import pytest

from contact import Contact
from controller import Controller
from exceptions import (
    PhoneAlreadyExists,
    PhoneNotExist,
)


def test_find_one(monkeypatch, capsys):
    """Проверяет успешный поиск контакта."""
    controller = Controller()
    contact = Contact("Иван", 111, "Работа")

    monkeypatch.setattr(
        controller.view, "ask_phone", lambda: 111
    )
    monkeypatch.setattr(
        controller.model, "find_contact",
        lambda phone: contact,
    )

    controller.find_one()

    captured = capsys.readouterr()
    assert "Иван" in captured.out
    assert "111" in captured.out


def test_find_one_phone_not_exist(monkeypatch, capsys):
    """Проверяет поиск несуществующего контакта."""
    controller = Controller()

    monkeypatch.setattr(
        controller.view, "ask_phone", lambda: 999
    )

    def fake_find_contact(phone):
        raise PhoneNotExist("Номер не найден")

    monkeypatch.setattr(
        controller.model, "find_contact",
        fake_find_contact,
    )

    controller.find_one()

    captured = capsys.readouterr()
    assert "Номер не найден" in captured.out
    assert "PhoneNotExist" in captured.out


def test_delete_one(monkeypatch, capsys):
    """Проверяет успешное удаление контакта."""
    controller = Controller()
    deleted_phones = []

    monkeypatch.setattr(
        controller.view, "ask_phone", lambda: 111
    )
    monkeypatch.setattr(
        controller.model, "delete_contact",
        lambda phone: deleted_phones.append(phone),
    )

    controller.delete_one()

    captured = capsys.readouterr()
    assert deleted_phones == [111]
    assert "Контакт удалён." in captured.out


def test_delete_one_phone_not_exist(monkeypatch, capsys):
    """Проверяет удаление несуществующего контакта."""
    controller = Controller()

    monkeypatch.setattr(
        controller.view, "ask_phone", lambda: 999
    )

    def fake_delete_contact(phone):
        raise PhoneNotExist("Телефон не найден")

    monkeypatch.setattr(
        controller.model, "delete_contact",
        fake_delete_contact,
    )

    controller.delete_one()

    captured = capsys.readouterr()
    assert "Телефон не найден" in captured.out
    assert "PhoneNotExist" in captured.out


def test_see_all(monkeypatch, capsys):
    """Проверяет вывод всех контактов."""
    controller = Controller()
    contacts = [
        Contact("Иван", 111, "Работа"),
        Contact("Анна", 222, "Дом"),
    ]

    monkeypatch.setattr(
        controller.model, "get_all",
        lambda: contacts,
    )

    controller.see_all()

    captured = capsys.readouterr()
    assert "Иван" in captured.out
    assert "111" in captured.out
    assert "Анна" in captured.out
    assert "222" in captured.out


def test_see_all_empty_directory(monkeypatch, capsys):
    """Проверяет вывод сообщения для пустого справочника."""
    controller = Controller()

    monkeypatch.setattr(
        controller.model, "get_all", lambda: []
    )

    controller.see_all()

    captured = capsys.readouterr()
    assert "Справочник пуст." in captured.out

def test_edit_one(monkeypatch, capsys):
    """Проверяет успешное редактирование контакта."""
    controller = Controller()
    edited_contacts = []

    monkeypatch.setattr(
        controller.view, "ask_phone", lambda: 111
    )
    monkeypatch.setattr(
        controller.view, "new_name", lambda: "Пётр"
    )
    monkeypatch.setattr(
        controller.view, "new_phone", lambda: 222
    )
    monkeypatch.setattr(
        controller.view, "new_comment", lambda: "Дом"
    )
    monkeypatch.setattr(
        controller.model, "find_contact",
        lambda phone: Contact("Иван", 111, "Работа"),
    )

    def fake_edit_contact(
        phone, new_name, new_phone, new_comment
    ):
        edited_contacts.append(
            (phone, new_name, new_phone, new_comment)
        )

    monkeypatch.setattr(
        controller.model, "edit_contact",
        fake_edit_contact,
    )

    controller.edit_one()

    captured = capsys.readouterr()
    assert edited_contacts == [(111, "Пётр", 222, "Дом")]
    assert "Контакт сохранён." in captured.out


def test_edit_one_phone_not_exist(monkeypatch, capsys):
    """Проверяет редактирование отсутствующего контакта."""
    controller = Controller()

    monkeypatch.setattr(
        controller.view, "ask_phone", lambda: 999
    )

    def fake_find_contact(phone):
        raise PhoneNotExist("Телефон не найден")

    monkeypatch.setattr(
        controller.model, "find_contact",
        fake_find_contact,
    )

    controller.edit_one()

    captured = capsys.readouterr()
    assert "Телефон не найден" in captured.out
    assert "PhoneNotExist" in captured.out


def test_edit_one_phone_already_exists(monkeypatch, capsys):
    """Проверяет обработку занятого нового номера."""
    controller = Controller()

    monkeypatch.setattr(
        controller.view, "ask_phone", lambda: 111
    )
    monkeypatch.setattr(
        controller.view, "new_name", lambda: "Пётр"
    )
    monkeypatch.setattr(
        controller.view, "new_phone", lambda: 222
    )
    monkeypatch.setattr(
        controller.view, "new_comment", lambda: "Дом"
    )
    monkeypatch.setattr(
        controller.model, "find_contact",
        lambda phone: Contact("Иван", 111, "Работа"),
    )

    def fake_edit_contact(
        phone, new_name, new_phone, new_comment
    ):
        raise PhoneAlreadyExists(
            "Такой номер уже существует"
        )

    monkeypatch.setattr(
        controller.model, "edit_contact",
        fake_edit_contact,
    )

    controller.edit_one()

    captured = capsys.readouterr()
    assert "Такой номер уже существует" in captured.out
    assert "PhoneAlreadyExists" in captured.out


def test_new_reg(monkeypatch, capsys):
    """Проверяет успешное добавление контакта."""
    controller = Controller()
    added_contacts = []

    monkeypatch.setattr(
        controller.view, "ask_phone", lambda: 111
    )
    monkeypatch.setattr(
        controller.view, "ask_name", lambda: "Иван"
    )
    monkeypatch.setattr(
        controller.view, "ask_comment", lambda: "Работа"
    )
    monkeypatch.setattr(
        controller.model, "phone_exists",
        lambda phone: False,
    )
    monkeypatch.setattr(
        controller.model, "add_contact",
        lambda contact: added_contacts.append(contact),
    )

    controller.new_reg()

    captured = capsys.readouterr()
    assert added_contacts == [
        Contact("Иван", 111, "Работа")
    ]
    assert "Номер добавлен." in captured.out


def test_new_reg_phone_already_exists(monkeypatch, capsys):
    """Проверяет добавление номера, который уже существует."""
    controller = Controller()

    monkeypatch.setattr(
        controller.view, "ask_phone", lambda: 111
    )
    monkeypatch.setattr(
        controller.model, "phone_exists",
        lambda phone: True,
    )

    controller.new_reg()

    captured = capsys.readouterr()
    assert "PhoneAlreadyExists" in captured.out


def test_new_reg_duplicate_in_directory(monkeypatch, capsys):
    """Проверяет обработку дубликата при добавлении."""
    controller = Controller()

    monkeypatch.setattr(
        controller.view, "ask_phone", lambda: 111
    )
    monkeypatch.setattr(
        controller.view, "ask_name", lambda: "Иван"
    )
    monkeypatch.setattr(
        controller.view, "ask_comment", lambda: "Работа"
    )
    monkeypatch.setattr(
        controller.model, "phone_exists",
        lambda phone: False,
    )

    def fake_add_contact(contact):
        raise PhoneAlreadyExists(
            "Такой номер уже существует"
        )

    monkeypatch.setattr(
        controller.model, "add_contact",
        fake_add_contact,
    )

    controller.new_reg()

    captured = capsys.readouterr()
    assert "Такой номер уже существует" in captured.out
    assert "PhoneAlreadyExists" in captured.out


def test_start_wrong_command(monkeypatch, capsys):
    """Проверяет обработку неправильной команды меню."""
    controller = Controller()
    actions = iter(["9", KeyboardInterrupt])

    def fake_menu():
        action = next(actions)
        if action is KeyboardInterrupt:
            raise KeyboardInterrupt
        return action

    monkeypatch.setattr(
        controller.view, "menu", fake_menu
    )

    with pytest.raises(KeyboardInterrupt):
        controller.start()

    captured = capsys.readouterr()
    assert "Неверная команда" in captured.out
    assert "WrongCommand" in captured.out
