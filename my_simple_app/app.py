import os.path

from my_framework.app import MyFrameworkApp
from my_framework.template_engine import MFTemplate

from my_simple_app.core.common import AppRouter
from my_simple_app.core.models import CourseCategory, OfflineCourse, OnlineCourse
from my_simple_app.core.views import ProxyView

from my_simple_app.middlewares import MyFCDater, MyLogger
from my_simple_app.views import PageViewController


class MyApp(MyFrameworkApp):
    def __init__(self, root_path: str):
        static_path = os.path.join(root_path, "statics")
        super().__init__("MyApp", statics_path=static_path)

        core_view = ProxyView()

        self.register_front(MyFCDater())
        self.register_front(MyLogger())

        for route, cls in AppRouter.routes.items():
            if issubclass(cls, PageViewController):
                self.register_view(route, cls(core_view))
            else:
                self.register_view(route, cls())

        MFTemplate.template_folder = os.path.join(root_path, "templates")

        # test {
        cc1 = CourseCategory("Базы данных")
        cc2 = CourseCategory("Офисные приложения")
        core_view.categories.add(cc1)
        core_view.categories.add(cc2)
        c1 = OfflineCourse("Postgres", cc1)
        c2 = OnlineCourse("Мой офис", cc2)
        core_view.courses.add(c1)
        core_view.courses.add(c2)
        # } test
