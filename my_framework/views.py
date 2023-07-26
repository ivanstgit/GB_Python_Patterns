from abc import abstractmethod
from typing import Tuple

from my_framework.exceptions import MFNotImplementedError
from my_framework.http_utils import ContentType, Request, Response, ResponseCode


class PageController:
    """Реализация паттерна PageController"""

    path_param = "path"

    def __call__(self, request: Request) -> Response:
        code, body = self.request(request)
        return Response(code, ContentType.TEXT_HTML, body.encode())

    @abstractmethod
    def request(self, request: Request) -> Tuple[str, str]:
        """return code, content"""
        raise MFNotImplementedError
