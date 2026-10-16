from contact import Contact


def test_create_contact() -> None:
    contact = Contact(
        name="Иван",
        phone=123456789,
        comment="Работа",
    )

    assert contact.name == "Иван"
    assert contact.phone == 123456789
    assert contact.comment == "Работа"