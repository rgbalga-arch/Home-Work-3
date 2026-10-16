import pytest
from view import View


def test_menu(monkeypatch, capsys):
    """Проверяет выбор пункта меню."""
    monkeypatch.setattr("builtins.input", lambda _: "3")

    view = View()

    assert view.menu() == "3"

    captured = capsys.readouterr()
    assert "3 - чтобы найти контакт" in captured.out


def test_ask_name(monkeypatch):
    """Проверяет ввод имени."""
    monkeypatch.setattr("builtins.input", lambda _: "Иван")

    view = View()

    assert view.ask_name() == "Иван"


def test_ask_phone(monkeypatch, capsys):
    """Проверяет ввод номера после неправильного значения."""
    values = iter(["abc", "123456"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(values)
    )

    view = View()

    assert view.ask_phone() == 123456

    captured = capsys.readouterr()
    assert "Введите только цифры" in captured.out
    assert "ValueError" in captured.out


def test_ask_comment(monkeypatch):
    """Проверяет ввод комментария."""
    monkeypatch.setattr("builtins.input", lambda _: "Друг")

    view = View()

    assert view.ask_comment() == "Друг"


def test_show_message(capsys):
    """Проверяет вывод сообщения."""
    view = View()

    view.show_message("Контакт сохранён.")

    captured = capsys.readouterr()
    assert "Контакт сохранён." in captured.out


def test_new_name(monkeypatch):
    """Проверяет ввод нового имени."""
    monkeypatch.setattr("builtins.input", lambda _: "Пётр")

    view = View()

    assert view.new_name() == "Пётр"


def test_new_phone(monkeypatch, capsys):
    """Проверяет повторный ввод нового номера."""
    values = iter(["ошибка", "987654"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(values)
    )

    view = View()

    assert view.new_phone() == 987654

    captured = capsys.readouterr()
    assert "Введите только цифры" in captured.out
    assert "ValueError" in captured.out


def test_new_comment(monkeypatch):
    """Проверяет ввод нового комментария."""
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "Коллега"
    )

    view = View()

    assert view.new_comment() == "Коллега"

@pytest.mark.parametrize(
    "name",
    ["Иван", "Ivan", "Иван Иванов", ""],
)
def test_ask_name(monkeypatch, capsys, name):
    monkeypatch.setattr("builtins.input", lambda _: name)

    view = View()

    assert view.ask_name() == name