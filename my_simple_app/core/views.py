from typing import Dict, List, Optional
from my_simple_app.core.common import Notifier, Observer, UniqueIdObject

from my_simple_app.core.exceptions import MyAppAlreadyExistsError
from my_simple_app.core.models import Course, CourseCategory, CourseUser, Student, User
from my_simple_app.core.notifiers import EmailNotifier, SmsNotifier


USER_NOTIFIERS = [SmsNotifier, EmailNotifier]


class ObjectStorage:
    storage: Dict[int, UniqueIdObject]
    ext_key_index: Dict[str, int]

    def __init__(self) -> None:
        self.storage = {}
        self.ext_key_index = {}

    def add(self, obj: UniqueIdObject, ext_key: str) -> UniqueIdObject:
        id = self.ext_key_index.get(ext_key, 0)
        if id:
            raise MyAppAlreadyExistsError

        id = max(self.storage.keys(), default=0) + 1
        obj.id = id
        self.storage[id] = obj
        self.ext_key_index[ext_key] = id
        return obj

    def get_by_id(self, id) -> Optional[UniqueIdObject]:
        return self.storage.get(id)

    def get_by_ext_key(self, name: str) -> Optional[UniqueIdObject]:
        id = self.ext_key_index.get(name, 0)
        return self.storage.get(id)

    def get_list(self) -> Optional[List[UniqueIdObject]]:
        return list(self.storage.values())


class CategoryView(ObjectStorage):
    def add(self, obj: CourseCategory) -> CourseCategory:
        return super().add(obj, obj.name)  # type: ignore

    def get_by_id(self, id) -> Optional[CourseCategory]:
        return super().get_by_id(id)  # type: ignore

    def get_by_name(self, name: str) -> Optional[CourseCategory]:
        return super().get_by_ext_key(name)  # type: ignore

    def get_list(self) -> Optional[List[CourseCategory]]:
        return super().get_list()  # type: ignore


class CourseUserView(ObjectStorage, Notifier):
    def __init__(self) -> None:
        ObjectStorage.__init__(self)
        Notifier.__init__(self)

    def add(self, obj: CourseUser) -> CourseUser:
        res = super().add(obj, obj.ext_key)
        self.notify()
        return res  # type: ignore

    def get_list_by_student(self, student: User) -> Optional[List[Course]]:
        if student:
            res = [
                course_user.course
                for course_user in self.storage.values()
                if isinstance(course_user, CourseUser)
                and course_user.user.id == student.id
            ]
            if res:
                return list(res)
        return super().get_list()  # type: ignore

    def get_list_by_course(self, course: Course) -> Optional[List[User]]:
        if course:
            res = [
                course_user.user
                for course_user in self.storage.values()
                if isinstance(course_user, CourseUser)
                and course_user.user.id == course.id
            ]
            if res:
                return list(res)
        return super().get_list()  # type: ignore


class CourseView(ObjectStorage, Observer):
    storage: Dict[int, Course]

    def add(self, obj: Course) -> Course:
        return super().add(obj, obj.name)  # type: ignore

    def get_by_id(self, id) -> Optional[Course]:
        return super().get_by_id(id)  # type: ignore

    def get_by_name(self, name: str) -> Optional[Course]:
        return super().get_by_ext_key(name)  # type: ignore

    def get_list(self, category: Optional[CourseCategory]) -> Optional[List[Course]]:
        if category:
            res = [
                course
                for course in self.storage.values()
                if isinstance(course, Course) and course.category.id == category.id
            ]
            if res:
                return list(res)
        return super().get_list()  # type: ignore

    def data_changed(self, notifier: CourseUserView):
        for course in self.storage.values():
            _students = notifier.get_list_by_course(course)
            if _students:
                course.students = _students
            else:
                course.students = []

    def notify_users(self, course: Course):
        for student in course.students:
            for notifier in USER_NOTIFIERS:
                notifier.notify(student, f"курс изменен {course.name}")


class StudentView(ObjectStorage, Observer):
    storage: Dict[int, Student]

    def add(self, obj: Student) -> Student:
        return super().add(obj, obj.name)  # type: ignore

    def get_by_id(self, id) -> Optional[Student]:
        return super().get_by_id(id)  # type: ignore

    def get_by_name(self, name: str) -> Optional[Student]:
        return super().get_by_ext_key(name)  # type: ignore

    def get_list(self) -> Optional[List[Student]]:
        return super().get_list()  # type: ignore

    def data_changed(self, notifier: CourseUserView):
        for student in self.storage.values():
            _courses = notifier.get_list_by_student(student)
            if _courses:
                student.courses = _courses
            else:
                student.courses = []


class ProxyView:
    def __init__(self) -> None:
        self._category_view = CategoryView()
        self._course_view = CourseView()
        self._student_view = StudentView()
        self._course_user_view = CourseUserView()

        # При изменении записи обновляем кеш в списке студентов
        self._course_user_view.add_observer(self._student_view)
        self._course_user_view.add_observer(self._course_view)

    @property
    def categories(self) -> CategoryView:
        return self._category_view

    @property
    def courses(self) -> CourseView:
        return self._course_view

    @property
    def students(self) -> StudentView:
        return self._student_view

    @property
    def course_students(self) -> CourseUserView:
        return self._course_user_view
