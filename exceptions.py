
class AppError(Exception):
    """Базовая ошибка приложения."""


class UserError(AppError):
    """Базовая ошибка, связанная с пользователем."""


class PhoneAlreadyExists(UserError):
    """Номер телефона уже существует."""


class OnlyNumbersError(AppError):
    """Номер телефона должен содержать только цифры."""


class FileNotExist(AppError):
    """Файл не существует."""


class PhoneNotExist(UserError):
    """Телефон не найден."""


class WrongCommand(AppError):
    """Введена неправильная команда."""
