from datetime import date

from my_framework.http_controller import Request
from my_framework.middleware_controller import FrontController

from my_simple_app.core.logger import Logger


class MyFCDater(FrontController):
    date = "date"

    def request(self, request: Request) -> None:
        request.custom_data[self.date] = date.today()


class MyLogger(FrontController):
    def request(self, request: Request) -> None:
        Logger("test").log(request)
