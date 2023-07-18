from datetime import date

from my_framework.middlewares import FrontController


class MyFCDater(FrontController):
    date = "date"

    def request(self, request: dict) -> None:
        request[self.date] = date.today()
