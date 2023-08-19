from my_simple_app.core.common import FileWriter, SingletonByName


class Logger(metaclass=SingletonByName):
    def __init__(self, name, writer=FileWriter("log.txt")):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f"log---> {text}"
        self.writer.write(text)
