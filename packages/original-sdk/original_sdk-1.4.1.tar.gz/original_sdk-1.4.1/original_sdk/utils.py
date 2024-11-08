import random
import string
from http import HTTPStatus


def get_random_string(length: int) -> str:
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for i in range(length))
    return random_string


def get_default_error_message(status_code: int) -> str:
    try:
        status = HTTPStatus(status_code)
        return status.phrase
    except ValueError:
        return "Unknown Error"
