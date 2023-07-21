from my_framework.http_utils import ResponseCode
from my_framework.templates import Template
from my_framework.views import PageController

from my_simple_app.middleware import MyFCDater


class MyIndexPage(PageController):
    def request(self, request):
        content = Template("index.html").render(date=request.get(MyFCDater.date))
        return ResponseCode.OK, content


class MyContactPage(PageController):
    def request(self, request):
        content = Template("contacts.html").render(date=request.get(MyFCDater.date))
        return ResponseCode.OK, content
