import os.path

from my_framework.http_utils import ContentType, Response, ResponseCode


class StaticsController:
    def __init__(self, static_folder: str) -> None:
        self.static_folder = static_folder

    def get(self, file_name: str) -> Response:
        file_path = os.path.join(self.static_folder, file_name)

        if not os.path.exists(file_path):
            return Response(ResponseCode.NOT_FOUND, ContentType.TEXT_HTML, b"")

        if file_name.endswith(".css"):
            content_type = ContentType.TEXT_CSS
            with open(file_path, mode="r", encoding="utf-8") as f:
                content = f.read().encode()
        elif file_name.endswith(".png"):
            content_type = ContentType.IMAGE_PNG
            with open(file_path, mode="rb") as f:
                content = f.read()
        else:
            return Response(ResponseCode.NOT_FOUND, ContentType.TEXT_HTML, b"")

        return Response(ResponseCode.OK, content_type, content)
