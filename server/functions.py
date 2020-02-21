from provider import services
from driver.models import Message


def check_is_expaired(m: Message):
    return m.is_expaired()


def clean_messageDB():
    services.messageDB.delete(func_checker=check_is_expaired)
