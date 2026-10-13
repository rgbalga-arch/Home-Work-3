from see_all import SeeAllList
from find_contact import ContFinder
from edit_contact import ContEditor
from delete_contct import DelContact
from new_contact import NewContact


class AppError(Exception):
    pass

class WrongCommand(AppError):
    pass

class Menu:

    while True:
        try:
            print("1 - чтобы добавить контакт")
            print("2 - чтобы посмотреть все контакты")
            print("3 - чтобы найти контакт")
            print("4 - чтобы изменить контакт")
            print("5 - чтобы удалить контакт")

            action_menu = input("Выберите действие: ")

            if action_menu == "1":
                NewContact().new_reg()
            elif action_menu == "2":
                SeeAllList().read_contacts()
            elif action_menu == "3":
                ContFinder().search_all()
            elif action_menu == "4":
                ContEditor().edit_contacts()
            elif action_menu == "5":
                DelContact().delete()
            else:
                raise WrongCommand("неверная команда")

        except WrongCommand as err:
            print(err)
            print(type(err).__name__)

