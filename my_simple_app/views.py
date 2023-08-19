from my_framework.http_controller import HTTPMethod, Request, ResponseCode
from my_framework.template_engine import MFTemplate
from my_framework.view_controller import PageController

from my_simple_app.core.common import AppRouter
from my_simple_app.core.views import ProxyView
from my_simple_app.core.exceptions import MyAppException
from my_simple_app.core.models import (
    CourseCategory,
    CourseFactory,
    CourseUser,
    OfflineCourse,
    OnlineCourse,
    Student,
)

from my_simple_app.middlewares import MyFCDater


class PageViewController(PageController):
    def __init__(self, core_view: ProxyView) -> None:
        super().__init__()
        self.core_view = core_view


@AppRouter("/")
class MyIndexPage(PageController):
    def request(self, request):
        content = MFTemplate("index.html").render(
            path=request.path,
            date=request.custom_data.get(MyFCDater.date),
        )
        return ResponseCode.OK, content


@AppRouter("/contacts/")
class MyContactPage(PageController):
    def request(self, request):
        content = MFTemplate("contacts.html").render(
            path=request.path,
            date=request.custom_data.get(MyFCDater.date),
        )
        return ResponseCode.OK, content


@AppRouter("/categories/")
class MyCategoryListPage(PageViewController):
    def request(self, request: Request):
        category_list = self.core_view.categories.get_list()

        content = MFTemplate("categories_list.html").render(
            path=request.path,
            category_list=category_list,
        )
        return ResponseCode.OK, content


@AppRouter("/categories/add/")
class MyCategoryAddPage(PageViewController):
    def request(self, request: Request):
        f_cat_name = ""
        f_errors = []
        if request.method == HTTPMethod.POST:
            f_cat_name = request.data.get("f_category_name")
            if f_cat_name:
                try:
                    cat = CourseCategory(f_cat_name)
                    self.core_view.categories.add(cat)
                    f_cat_name = ""
                except MyAppException as exc:
                    f_errors = [str(exc)]

        content = MFTemplate("categories_add.html").render(
            path=request.path,
            f_category_name=f_cat_name,
            f_errors=f_errors,
        )
        return ResponseCode.OK, content


@AppRouter("/courses/")
class MyCourseListPage(PageViewController):
    def request(self, request: Request):
        # filters:
        category = None
        category_id = request.data.get("category_id", "")
        if category_id:
            try:
                category = self.core_view.categories.get_by_id(int(category_id))
            except Exception as exc:
                category = None

        course_list = self.core_view.courses.get_list(category)

        content = MFTemplate("courses_list.html").render(
            path=request.path,
            category=category,
            course_list=course_list,
        )
        return ResponseCode.OK, content


@AppRouter("/courses/add/")
class MyCourseAddPage(PageViewController):
    def request(self, request: Request):
        # form fields:
        f_course_name = ""
        f_category_id = ""
        f_type_id = ""
        f_category_list = self.core_view.categories.get_list()
        f_type_list = CourseFactory.get_types()
        f_errors = []

        if request.method == HTTPMethod.POST:
            f_course_name = request.data.get("f_course_name")
            f_category_id = request.data.get("f_category_id")
            f_type_id = request.data.get("f_type_id")

            if f_course_name and f_category_id and f_type_id:
                try:
                    cat = self.core_view.categories.get_by_id(int(f_category_id))
                    if not cat:
                        raise MyAppException
                    course = CourseFactory.create(
                        type_=f_type_id, name=f_course_name, category=cat
                    )
                    self.core_view.courses.add(course)

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


@AppRouter("/courses/edit/")
class MyCourseEditPage(PageViewController):
    def request(self, request: Request):
        # form fields:
        course_id = request.data.get("id")
        if course_id:
            course = self.core_view.courses.get_by_id(int(course_id))
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

                    self.core_view.courses.notify_users(course)

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


@AppRouter("/students/")
class MyStudentListPage(PageViewController):
    def request(self, request: Request):
        student_list = self.core_view.students.get_list()

        content = MFTemplate("students_list.html").render(
            path=request.path,
            student_list=student_list,
        )
        return ResponseCode.OK, content


@AppRouter("/students/add/")
class MyStudentAddPage(PageViewController):
    def request(self, request: Request):
        f_student_name = ""
        f_errors = []
        if request.method == HTTPMethod.POST:
            f_student_name = request.data.get("f_student_name")
            if f_student_name:
                try:
                    student = Student(f_student_name)
                    self.core_view.students.add(student)
                    f_student_name = ""
                except MyAppException as exc:
                    f_errors = [str(exc)]

        content = MFTemplate("students_add.html").render(
            path=request.path,
            f_student_name=f_student_name,
            f_errors=f_errors,
        )
        return ResponseCode.OK, content


@AppRouter("/students/add_course/")
class MyStudentAddCoursePage(PageViewController):
    def request(self, request: Request):
        f_course_list = self.core_view.courses.get_list(None)
        f_student_list = self.core_view.students.get_list()
        f_errors = []

        if request.method == HTTPMethod.POST:
            f_course_id = request.data.get("f_course_id")
            f_student_id = request.data.get("f_student_id")
            if f_student_id and f_course_id:
                try:
                    course = self.core_view.courses.get_by_id(int(f_course_id))
                    student = self.core_view.students.get_by_id(int(f_student_id))
                    cu = CourseUser(course, student)  # type: ignore
                    self.core_view.course_students.add(cu)
                    f_course_id = ""
                except MyAppException as exc:
                    f_errors = [str(exc)]
        else:
            course_id = request.data.get("course_id")
            student_id = request.data.get("student_id")
            # if course_id:
            #     course = self.core_view.courses.get_by_id(int(course_id))
            # else:
            #     course = None
            # if student_id:
            #     student = self.core_view.students.get_by_id(int(student_id))
            # else:
            #     student = None
            f_course_id = course_id
            f_student_id = student_id

        content = MFTemplate("students_add_course.html").render(
            path=request.path,
            f_course_id=f_course_id,
            f_course_list=f_course_list,
            f_student_id=f_student_id,
            f_student_list=f_student_list,
            f_errors=f_errors,
        )
        return ResponseCode.OK, content
