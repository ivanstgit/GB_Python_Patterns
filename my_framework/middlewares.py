from my_framework.exceptions import MFNotImplementedError


class FrontController:
    """Реализация паттерна FrontController"""

    def __call__(self, request: dict) -> None:
        self.request(request)

    def request(self, request) -> None:
        raise MFNotImplementedError
