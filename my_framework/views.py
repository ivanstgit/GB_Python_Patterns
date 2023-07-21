from typing import Tuple

from my_framework.exceptions import MFNotImplementedError
from my_framework.http_utils import ContentType, Response, ResponseCode


class PageController:
    """Реализация паттерна PageController"""

    def __call__(self, request: dict) -> Response:
        code, body = self.request(request)
        return Response(code, ContentType.TEXT_HTML, body.encode())

    def request(self, request) -> Tuple[str, str]:
        """return code, content"""
        raise MFNotImplementedError
