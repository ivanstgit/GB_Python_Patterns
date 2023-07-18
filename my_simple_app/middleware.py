from datetime import date
from typing_extensions import override

from my_framework.middlewares import FrontController


class MyFCDater(FrontController):
    date = "date"

    @override
    def request(self, request: dict) -> None:
        request[self.date] = date.today()
