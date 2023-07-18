from typing import Dict, List

from my_framework.exceptions import MFalreadyRegisteredError
from my_framework.http_utils import Request, Response404
from my_framework.middlewares import FrontController
from my_framework.statics import StaticsController
from my_framework.views import PageController


class MyFrameworkApp:
    """Класс приложения"""

    _routes: Dict[str, PageController]
    _fronts: List[FrontController]
    """ path, page controller"""

    def __init__(
        self, name: str, statics_route_prefix="/statics/", statics_path="static"
    ):
        self._name = name
        self._routes = {}
        self._fronts = []
        self._statics_route_prefix = statics_route_prefix
        self.statics = StaticsController(statics_path)

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
        path = str(environ["PATH_INFO"])

        if path.startswith(self._statics_route_prefix):
            statics_path = path.replace(self._statics_route_prefix, "")
            response = self.statics.get(statics_path)

        else:
            # добавление закрывающего слеша
            if not path.endswith("/"):
                path = path + "/"

            # находим нужный контроллер
            # отработка паттерна page controller
            view = self._routes.get(path, None)
            if view:
                # обрабатываем параметры запроса
                req = Request(environ)
                request = {"method": req.method, "data": req.data}
                print(f"request {request}")

                # наполняем словарь request элементами
                # этот словарь получат все контроллеры
                # отработка паттерна front controller
                for front in self._fronts:
                    front(request)

                # запуск контроллера с передачей объекта request
                response = view(request)
            else:
                response = Response404()

        start_response(response.code, [response.header])
        return [response.content]

    def run(self, host="", port=8080):
        from wsgiref.simple_server import make_server

        with make_server(host, port, self) as httpd:
            print(f"Запуск на порту {port}...")
            httpd.serve_forever()
