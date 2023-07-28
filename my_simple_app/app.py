import os.path

from my_framework.app import MyFrameworkApp
from my_framework.template_engine import MFTemplate
from my_simple_app.core.controllers import CourseCategoryController, CourseController
from my_simple_app.core.models import (
    CourseCategory,
    Course,
    OfflineCourse,
    OnlineCourse,
)

from my_simple_app.middlewares import MyFCDater, MyLogger
from my_simple_app.views import (
    MyCategoryListPage,
    MyCategoryAddPage,
    MyCourseEditPage,
    MyCourseListPage,
    MyCourseAddPage,
    MyIndexPage,
    MyContactPage,
)


class MyApp(MyFrameworkApp):
    def __init__(self, root_path: str):
        static_path = os.path.join(root_path, "statics")
        super().__init__("MyApp", statics_path=static_path)

        category_controller = CourseCategoryController()
        course_controller = CourseController()

        # test {
        cc1 = CourseCategory("Базы данных")
        cc2 = CourseCategory("Офисные приложения")
        category_controller.add(cc1)
        category_controller.add(cc2)
        c1 = OfflineCourse("Postgres", cc1)
        c2 = OnlineCourse("Мой офис", cc2)
        course_controller.add(c1)
        course_controller.add(c2)
        # } test

        self.register_front(MyFCDater())
        self.register_front(MyLogger())

        self.register_view("/", MyIndexPage())
        self.register_view("/contacts/", MyContactPage())
        self.register_view("/categories/", MyCategoryListPage(category_controller))
        self.register_view("/categories/add/", MyCategoryAddPage(category_controller))
        self.register_view(
            "/courses/", MyCourseListPage(category_controller, course_controller)
        )
        self.register_view(
            "/courses/add/", MyCourseAddPage(category_controller, course_controller)
        )
        self.register_view(
            "/courses/edit/", MyCourseEditPage(category_controller, course_controller)
        )

        MFTemplate.template_folder = os.path.join(root_path, "templates")
