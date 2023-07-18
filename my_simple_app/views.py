from typing_extensions import override

from my_framework.templates import Template
from my_framework.views import PageController as PC, ResponseCodes as RC

from my_simple_app.middleware import MyFCDater


class MyIndexPage(PC):
    @override
    def request(self, request):
        content = Template("index.html").render(date=request.get(MyFCDater.date))
        return RC.OK, content


class MyContactPage(PC):
    @override
    def request(self, request):
        content = Template("contacts.html").render(date=request.get(MyFCDater.date))
        return RC.OK, content
