from jinja2 import (
    Environment as JinjaEnvironment,
    Template as JinjaTemplate,
    FileSystemLoader as JinjaLoader,
)


class MFTemplate:
    template_folder = "templates"
    template: JinjaTemplate

    def __init__(self, template_name: str):
        env = JinjaEnvironment(
            loader=JinjaLoader(self.template_folder), autoescape=True
        )
        self.template = env.get_template(template_name)

    def render(self, *args, **kwargs):
        return self.template.render(*args, **kwargs)
