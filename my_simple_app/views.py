from my_framework.http_utils import ResponseCode
from my_framework.templates import MFTemplate
from my_framework.views import PageController

from my_simple_app.middleware import MyFCDater


class MyIndexPage(PageController):
    def request(self, request):
        content = MFTemplate("index.html").render(
            date=request.custom_data.get(MyFCDater.date), path=request.path
        )
        return ResponseCode.OK, content


class MyContactPage(PageController):
    def request(self, request):
        content = MFTemplate("contacts.html").render(
            date=request.custom_data.get(MyFCDater.date), path=request.path
        )
        return ResponseCode.OK, content
