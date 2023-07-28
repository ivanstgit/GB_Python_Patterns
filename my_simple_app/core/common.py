from copy import deepcopy

from my_framework.view_controller import PageController


class SingletonByName(type):
    # порождающий паттерн Синглтон
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        elif kwargs:
            name = kwargs["name"]
        else:
            name = None

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class UniqueIdObject:
    id: int

    def __init__(self) -> None:
        self.id = 0

    def has_id(self) -> bool:
        return self.id > 0


class PrototypeMixin:
    # прототип
    def clone(self):
        obj = deepcopy(self)
        if isinstance(obj, UniqueIdObject):
            obj.id = 0
        return obj


class AppRouter:
    routes = {}

    def __init__(self, url: str):
        """
        Сохраняем значение переданного параметра
        """
        self.url = url

    def __call__(self, cls):
        """
        Сам декоратор
        """
        self.routes[self.url] = cls
