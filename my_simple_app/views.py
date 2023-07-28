from my_framework.http_controller import HTTPMethod, Request, ResponseCode
from my_framework.template_engine import MFTemplate
from my_framework.view_controller import PageController
from my_simple_app.core.controllers import CourseCategoryController, CourseController
from my_simple_app.core.exceptions import MyAppException
from my_simple_app.core.models import (
    Course,
    CourseCategory,
    CourseFactory,
    OfflineCourse,
    OnlineCourse,
)

from my_simple_app.middlewares import MyFCDater


class MyIndexPage(PageController):
    def request(self, request):
        content = MFTemplate("index.html").render(
            path=request.path,
            date=request.custom_data.get(MyFCDater.date),
        )
        return ResponseCode.OK, content


class MyContactPage(PageController):
    def request(self, request):
        content = MFTemplate("contacts.html").render(
            path=request.path,
            date=request.custom_data.get(MyFCDater.date),
        )
        return ResponseCode.OK, content


class MyCategoryListPage(PageController):
    def __init__(self, controller: CourseCategoryController) -> None:
        super().__init__()
        self.controller = controller

    def request(self, request: Request):
        category_list = self.controller.get_list()

        content = MFTemplate("categories_list.html").render(
            path=request.path,
            category_list=category_list,
        )
        return ResponseCode.OK, content


class MyCategoryAddPage(PageController):
    def __init__(self, controller: CourseCategoryController) -> None:
        super().__init__()
        self.controller = controller

    def request(self, request: Request):
        f_cat_name = ""
        f_errors = []
        if request.method == HTTPMethod.POST:
            f_cat_name = request.data.get("f_category_name")
            if f_cat_name:
                try:
                    cat = CourseCategory(f_cat_name)
                    self.controller.add(cat)
                    f_cat_name = ""
                except MyAppException as exc:
                    f_errors = [str(exc)]

        content = MFTemplate("categories_add.html").render(
            path=request.path,
            f_category_name=f_cat_name,
            f_errors=f_errors,
        )
        return ResponseCode.OK, content


class MyCourseListPage(PageController):
    def __init__(
        self,
        cat_controller: CourseCategoryController,
        course_controller: CourseController,
    ) -> None:
        super().__init__()
        self.course_controller = course_controller
        self.cat_controller = cat_controller

    def request(self, request: Request):
        # filters:
        category = None
        category_id = request.data.get("category_id", "")
        if category_id:
            try:
                category = self.cat_controller.get_by_id(int(category_id))
            except Exception as exc:
                category = None

        course_list = self.course_controller.get_list(category)

        content = MFTemplate("courses_list.html").render(
            path=request.path,
            category=category,
            course_list=course_list,
        )
        return ResponseCode.OK, content


class MyCourseAddPage(PageController):
    def __init__(
        self,
        cat_controller: CourseCategoryController,
        course_controller: CourseController,
    ) -> None:
        super().__init__()
        self.course_controller = course_controller
        self.cat_controller = cat_controller

    def request(self, request: Request):
        # form fields:
        f_course_name = ""
        f_category_id = ""
        f_type_id = ""
        f_category_list = self.cat_controller.get_list()
        f_type_list = CourseFactory.get_types()
        f_errors = []

        if request.method == HTTPMethod.POST:
            f_course_name = request.data.get("f_course_name")
            f_category_id = request.data.get("f_category_id")
            f_type_id = request.data.get("f_type_id")

            if f_course_name and f_category_id and f_type_id:
                try:
                    cat = self.cat_controller.get_by_id(int(f_category_id))
                    if not cat:
                        raise MyAppException
                    course = CourseFactory.create(
                        type_=f_type_id, name=f_course_name, category=cat
                    )
                    self.course_controller.add(course)

                    redirect_url = f"/courses/edit/?course_id={course.id}"

                    content = MFTemplate("_redirect.html").render(url=redirect_url)
                    return ResponseCode.OK, content

                except MyAppException as exc:
                    f_errors = [str(exc)]
            else:
                f_errors = ["Не заполнены обязательные поля формы"]

        content = MFTemplate("courses_add.html").render(
            path=request.path,
            f_course_name=f_course_name,
            f_category_id=f_category_id,
            f_category_list=f_category_list,
            f_type_list=f_type_list,
            f_errors=f_errors,
        )
        return ResponseCode.OK, content


class MyCourseEditPage(PageController):
    def __init__(
        self,
        cat_controller: CourseCategoryController,
        course_controller: CourseController,
    ) -> None:
        super().__init__()
        self.course_controller = course_controller
        self.cat_controller = cat_controller

    def request(self, request: Request):
        # form fields:
        course_id = request.data.get("id")
        if course_id:
            course = self.course_controller.get_by_id(int(course_id))
        else:
            course = None
        f_errors = []

        if course:
            if request.method == HTTPMethod.POST:
                try:
                    if isinstance(course, OnlineCourse):
                        f_webinar_system = request.data.get("f_webinar_system")
                        if f_webinar_system:
                            course.webinar_system = f_webinar_system

                    elif isinstance(course, OfflineCourse):
                        f_address = request.data.get("f_address")
                        if f_address:
                            course.address = f_address

                    content = MFTemplate("_redirect.html").render(url="/courses/")
                    return ResponseCode.OK, content

                except MyAppException as exc:
                    f_errors = [str(exc)]

            if isinstance(course, OnlineCourse):
                content = MFTemplate("courses_edit_online.html").render(
                    path=request.path,
                    course=course,
                    f_errors=f_errors,
                )
            elif isinstance(course, OfflineCourse):
                content = MFTemplate("courses_edit_offline.html").render(
                    path=request.path,
                    course=course,
                    f_errors=f_errors,
                )
            else:
                content = MFTemplate("_redirect.html").render(url="/courses/")
        else:
            f_errors = ["Не заполнены обязательные поля формы"]
            content = MFTemplate("_redirect.html").render(url="/courses/")

        return ResponseCode.OK, content
