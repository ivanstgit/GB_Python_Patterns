import os.path

from my_framework.app import MyFrameworkApp
from my_framework.templates import Template

from my_simple_app.middleware import MyFCDater
from my_simple_app.views import MyIndexPage, MyContactPage


class MyApp(MyFrameworkApp):
    def __init__(self, root_path: str):
        static_path = os.path.join(root_path, "static")
        super().__init__("MyApp", statics_path=static_path)

        self.register_front(MyFCDater())

        self.register_view("/", MyIndexPage())
        self.register_view("/index/", MyIndexPage())
        self.register_view("/contacts/", MyContactPage())

        Template.template_folder = os.path.join(root_path, "templates")
