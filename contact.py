from dataclasses import dataclass


@dataclass
class Contact:
    """Представляет один контакт телефонного справочника."""

    name: str
    phone: int
    comment: str