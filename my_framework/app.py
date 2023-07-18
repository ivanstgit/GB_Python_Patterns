from typing import Dict, List

from my_framework.middlewares import FrontController
from my_framework.views import PageController, PageNotFound404
from my_framework.exceptions import MFalreadyRegisteredError


class MyFrameworkApp:
    """Класс приложения"""

    _routes: Dict[str, PageController]
    _fronts: List[FrontController]
    """ path, page controller"""

    def __init__(self, name: str):
        self._name = name
        self._routes = {}
        self._fronts = []

    def register_front(self, fc: FrontController) -> None:
        if fc in self._fronts:
            raise MFalreadyRegisteredError
        self._fronts.append(fc)

    def register_view(self, route: str, view: PageController) -> None:
        _ = self._routes.get(route, None)
        if _:
            raise MFalreadyRegisteredError
        else:
            self._routes[route] = view

    def __call__(self, environ: dict, start_response) -> List[bytes]:
        # получаем адрес, по которому выполнен переход
        path = environ["PATH_INFO"]

        # добавление закрывающего слеша
        if not path.endswith("/"):
            path = path + "/"

        # находим нужный контроллер
        # отработка паттерна page controller
        view = self._routes.get(path, PageNotFound404())

        request = {}
        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self._fronts:
            front(request)

        # запуск контроллера с передачей объекта request
        code, body = view(request)

        start_response(code, [("Content-Type", "text/html")])
        return [body.encode("utf-8")]

    def run(self, host="", port=8080):
        from wsgiref.simple_server import make_server

        with make_server(host, port, self) as httpd:
            print(f"Запуск на порту {port}...")
            httpd.serve_forever()
