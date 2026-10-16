try:
    if not self.model.phone_exists(phone):
        raise PhoneNotExist()
except PhoneNotExist as err:
    self.view.show_message(str(err))
    print(type(err).__name__)
    return

