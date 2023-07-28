from typing import Dict, List, Optional

from my_simple_app.core.exceptions import MyAppAlreadyExistsError
from my_simple_app.core.models import Course, CourseCategory


class CategoryView:
    storage: Dict[int, CourseCategory]
    ext_key_index: Dict[str, int]

    def __init__(self) -> None:
        self.storage = {}
        self.ext_key_index = {}

    def add(self, obj: CourseCategory) -> CourseCategory:
        ext_key = obj.name

        id = self.ext_key_index.get(ext_key, 0)
        if id:
            raise MyAppAlreadyExistsError

        id = max(self.storage.keys(), default=0) + 1
        obj.id = id
        self.storage[id] = obj
        self.ext_key_index[ext_key] = id
        return obj

    def get_by_id(self, id) -> Optional[CourseCategory]:
        return self.storage.get(id)

    def get_by_name(self, name: str) -> Optional[CourseCategory]:
        id = self.ext_key_index.get(name, 0)
        return self.storage.get(id)

    def get_list(self) -> Optional[List[CourseCategory]]:
        return list(self.storage.values())


class CourseView:
    storage: Dict[int, Course]
    ext_key_index: Dict[str, int]

    def __init__(self) -> None:
        self.storage = {}
        self.ext_key_index = {}

    def add(self, obj: Course) -> Course:
        ext_key = obj.name

        id = self.ext_key_index.get(ext_key, 0)
        if id:
            raise MyAppAlreadyExistsError

        id = max(self.storage.keys(), default=0) + 1
        obj.id = id
        self.storage[id] = obj
        self.ext_key_index[ext_key] = id
        return obj

    def get_by_id(self, id) -> Optional[Course]:
        return self.storage.get(id)

    def get_by_name(self, name: str) -> Optional[Course]:
        id = self.ext_key_index.get(name, 0)
        return self.storage.get(id)

    def get_list(self, category: Optional[CourseCategory]) -> Optional[List[Course]]:
        if category:
            res = [
                course
                for course in self.storage.values()
                if course.category.id == category.id
            ]
            if res:
                return list(res)
        return list(self.storage.values())


class ProxyView:
    def __init__(self) -> None:
        self._category_view = None
        self._course_view = None

    @property
    def categories(self) -> CategoryView:
        if not self._category_view:
            self._category_view = CategoryView()
        return self._category_view

    @property
    def courses(self) -> CourseView:
        if not self._course_view:
            self._course_view = CourseView()
        return self._course_view
