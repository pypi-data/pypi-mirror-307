from jinja2 import Environment, FileSystemLoader
from typing import List
from .cli_parser import CommandOption

class WebGenerator:
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader('cli2web/templates')
        )
        
    def generate_form(self, command_name: str, options: List[CommandOption]) -> str:
        """生成HTML表单"""
        template = self.env.get_template('cli_form.html')
        return template.render(
            command_name=command_name,
            options=options
        ) 