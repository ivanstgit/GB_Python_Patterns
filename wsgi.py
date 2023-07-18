import os

from my_simple_app.app import MyApp


application = MyApp(os.path.join(os.getcwd(), "my_simple_app"))

if __name__ == "__main__":
    application.run()
