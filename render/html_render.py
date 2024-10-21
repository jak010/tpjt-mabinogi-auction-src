from datetime import datetime

from jinja2 import Template
import os


class HtmlRender:

    def __init__(self,
                 title,
                 reports,
                 reports_json
                 ):
        self.project_root = os.path.dirname(os.path.abspath(__file__))

        self.title = title
        self.reports = reports
        self.reports_json = reports_json

        self._template_path = self.project_root + "/templates/report.html"
        self._output_path = self.project_root + "/output/temp.html"

    def execute(self):
        with open(self._template_path, "r") as f:
            template = Template(f.read())

            html_content = template.render(
                title=self.title,
                reports=self.reports,
                reports_json=self.reports_json,
                date=datetime.now().strftime('%Y-%m-%d')
            )

            self._save(html_content)

    def _save(self, html_content):
        with open(self._output_path, "w", encoding="utf-8") as f2:
            f2.write(html_content)
