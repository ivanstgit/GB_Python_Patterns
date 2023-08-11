from abc import abstractmethod
from typing import List

from my_simple_app.core.common import Observer
from my_simple_app.core.models import Course, User


class UserNotifier:
    @staticmethod
    def notify(user: User, msg: str):
        pass


class SmsNotifier(UserNotifier):
    @staticmethod
    def notify(user: User, msg: str):
        print(f"SMS-> {user.name}: {msg}")


class EmailNotifier(UserNotifier):
    @staticmethod
    def notify(user: User, msg: str):
        print(f"Email-> {user.name}: {msg}")
