from typing import Tuple
from typing_extensions import override

from my_framework.exceptions import MFNotImplementedError


class PageController:
    """Реализация паттерна PageController"""

    def __call__(self, request: dict) -> Tuple[str, str]:
        return self.request(request)

    def request(self, request) -> Tuple[str, str]:
        raise MFNotImplementedError


class PageNotFound404(PageController):
    @override
    def request(self, request):
        return ResponseCodes.NOT_FOUND, "404 PAGE Not Found"


class ResponseCodes:
    OK = "200 OK"
    NOT_FOUND = "404 WHAT"
