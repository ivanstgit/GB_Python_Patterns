from jinja2 import Template as JinjaTemplate
import os.path


class Template:
    template_folder = "templates"
    template: JinjaTemplate

    def __init__(self, template_name: str):
        file_path = os.path.join(self.template_folder, template_name)

        with open(file_path, encoding="utf-8") as f:
            self.template = JinjaTemplate(f.read())

    def render(self, *args, **kwargs):
        return self.template.render(*args, **kwargs)
