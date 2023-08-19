from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List

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


# поведенческий паттерн - Стратегия
class ConsoleWriter:
    def write(self, text):
        print(text)


class FileWriter:
    def __init__(self, filename: str):
        self.file_name = filename

    def write(self, text):
        with open(self.file_name, "a", encoding="utf-8") as f:
            f.write(f"{text}\n")


# поведенческий паттерн - наблюдатель
class Observer(ABC):
    @abstractmethod
    def data_changed(self, notifier):
        pass


class Notifier:
    _observers: List[Observer]

    def __init__(self):
        self._observers = []

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def notify(self):
        for item in self._observers:
            item.data_changed(self)
