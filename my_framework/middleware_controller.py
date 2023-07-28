from abc import abstractmethod

from my_framework.exceptions import MFNotImplementedError
from my_framework.http_controller import Request


class FrontController:
    """Реализация паттерна FrontController"""

    def __call__(self, request: Request) -> None:
        self.request(request)

    @abstractmethod
    def request(self, request: Request) -> None:
        raise MFNotImplementedError
