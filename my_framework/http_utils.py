from typing import Optional

# from quopri import decodestring
import urllib.parse

ENCODING = "utf-8"


class ContentType:
    TEXT_HTML = "text/html"
    TEXT_CSS = "text/css"
    IMAGE_PNG = "image/png"


class HTTPMethod:
    GET = "GET"
    POST = "POST"


class ResponseCode:
    OK = "200 OK"
    NOT_FOUND = "404 WHAT"


class Request:
    def __init__(self, env: dict) -> None:
        self._env = env
        self._method = env.get("REQUEST_METHOD", None)
        self._data = {}
        if self._method == HTTPMethod.GET:
            self._data = self._get_data_from_query_string()
        elif self._method == HTTPMethod.POST:
            self._data = self._get_data_from_input()

    @property
    def method(self) -> Optional[str]:
        return self._method

    @property
    def data(self) -> dict:
        return self._data

    def _get_data_from_query_string(self) -> dict:
        query_string = self._env.get("QUERY_STRING", None)
        if query_string:
            return self._parse_string(query_string)
        return {}

    def _get_data_from_input(self) -> dict:
        content_len_str = self._env.get("CONTENT_LENGTH")
        if not content_len_str:
            return {}
        content_len = int(content_len_str)
        wsgi_input = self._env["wsgi.input"].read(content_len).decode(ENCODING)
        return self._parse_string(wsgi_input)

    def _parse_string(self, input: str) -> dict:
        result = {}
        params = input.split("&")
        for item in params:
            k, v = item.split("=")
            result[k] = self._decode_value(v)
        return result

    def _decode_value(self, val: str):
        if self._method == HTTPMethod.GET:
            res = urllib.parse.unquote(val)
        else:
            res = urllib.parse.unquote_plus(val)
        # val_b = bytes(val.replace("%", "=").replace("+", " "), ENCODING)
        # res = decodestring(val).decode(ENCODING)
        return res


class Response:
    def __init__(self, code: str, content_type: str, content: bytes) -> None:
        self.code = code
        self.content_type = content_type
        self.content = content

    @property
    def header(self) -> tuple:
        return ("Content-Type", self.content_type)


class Response404(Response):
    def __init__(self) -> None:
        super().__init__(ResponseCode.NOT_FOUND, ContentType.TEXT_HTML, b"")
