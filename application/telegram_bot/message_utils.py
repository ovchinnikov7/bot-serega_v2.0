
division_remainder = (2, 3, 4)

def get_word_form(count):
    if (count % 10 in division_remainder):
        return 'раза'
    else:
        return 'раз'


def get_user_first_name(message):
    user_name = message.from_user.first_name
    if user_name is None:
        user_name = message.from_user.username
    return user_name


def get_text(message):
    return str(message.text).lower()


def get_user_id(message):
    return str(message.from_user.id)


def is_contain(text, words):
    text_lower_case = text.lower()
    for word in words:
        if text_lower_case.find(word) != -1: return True
    return False