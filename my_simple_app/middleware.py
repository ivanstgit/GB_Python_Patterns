from datetime import date

from my_framework.http_utils import Request
from my_framework.middlewares import FrontController


class MyFCDater(FrontController):
    date = "date"

    def request(self, request: Request) -> None:
        request.custom_data[self.date] = date.today()
