from typing import Dict, List, Optional
from my_simple_app.core.common import PrototypeMixin, UniqueIdObject


class CourseType:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


class CourseCategory(UniqueIdObject):
    def __init__(self, name: str):
        super().__init__()
        self.name = name


class Course(UniqueIdObject, PrototypeMixin):
    def __init__(self, name: str, category: CourseCategory, type_: CourseType):
        super().__init__()
        self.name = name
        self.category = category
        self.course_type = type_


# онлайн курсы (вебинары), для них указывается вебинарная система
class OnlineCourse(Course):
    course_type = "online"

    def __init__(self, name: str, category: CourseCategory):
        super().__init__(
            name, category, CourseFactory.get_type(self.course_type)  # type: ignore
        )
        self.webinar_system = ""


# офлайн (в живую) курсы (для них указывается адрес проведения)
class OfflineCourse(Course):
    course_type = "offline"

    def __init__(self, name: str, category: CourseCategory):
        super().__init__(
            name, category, CourseFactory.get_type(self.course_type)  # type: ignore
        )
        self.address = ""


class CourseFactory:
    types = {
        OnlineCourse.course_type: ("Онлайн", OnlineCourse),
        OfflineCourse.course_type: ("Офлайн", OfflineCourse),
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_: str, name: str, category: CourseCategory) -> Course:
        c_type = cls.types[type_]
        res = c_type[1](name, category)
        res.course_type = CourseType(type_, c_type[0])
        return res

    @classmethod
    def get_type(cls, type_: str) -> Optional[CourseType]:
        c_type = cls.types.get(type_, None)
        if c_type:
            return CourseType(type_, c_type[0])
        return None

    @classmethod
    def get_types(cls) -> List[CourseType]:
        res = [CourseType(k, v[0]) for k, v in cls.types.items()]
        return list(res)


# абстрактный пользователь
class User(UniqueIdObject):
    pass


# преподаватель
class Teacher(User):
    pass


# студент
class Student(User):
    pass


class UserFactory:
    types = {
        "student": Student,
        "teacher": Teacher,
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()
