class View:
    """Отвечает за ввод данных и вывод сообщений пользователю."""

    def menu(self) -> str:
        """Показывает меню и возвращает выбранное действие."""
        print("1 - чтобы добавить контакт")
        print("2 - чтобы посмотреть все контакты")
        print("3 - чтобы найти контакт")
        print("4 - чтобы изменить контакт")
        print("5 - чтобы удалить контакт")

        action_menu = input("Выберите действие: ")
        return action_menu

    def ask_name(self) -> str:
        """Запрашивает имя контакта."""
        name = input("Введите имя: ")
        return name

    def ask_phone(self) -> int:
        """Запрашивает номер телефона и проверяет ввод."""
        while True:
            try:
                phone = int(input("Введите номер телефона: "))
                return phone
            except ValueError as err:
                self.show_message("Введите только цифры")
                print(type(err).__name__)

    def ask_comment(self) -> str:
        """Запрашивает комментарий к контакту."""
        comment = input("Введите комментарий: ")
        return comment

    def show_message(self, message: str) -> None:
        """Выводит сообщение пользователю."""
        print(message)

    def new_name(self) -> str:
        """Запрашивает новое имя контакта."""
        new_name = input("Введите новое имя: ")
        return new_name

    def new_phone(self) -> int:
        """Запрашивает новый номер телефона и проверяет ввод."""
        while True:
            try:
                new_phone = int(input("Введите новый номер телефона: "))
                return new_phone
            except ValueError as err:
                self.show_message("Введите только цифры")
                print(type(err).__name__)

    def new_comment(self) -> str:
        """Запрашивает новый комментарий."""
        new_comment = input("Введите новый комментарий: ")
        return new_comment