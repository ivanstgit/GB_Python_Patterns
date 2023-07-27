from my_simple_app.core.common import SingletonByName


class Logger(metaclass=SingletonByName):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print("log--->", text)
