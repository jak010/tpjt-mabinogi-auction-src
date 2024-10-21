from html2image import Html2Image
from pathlib import Path
import os


class HtmlImageExporter:

    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))

        self._read_html_path = self.project_root + "/output/temp.html"
        self._read_css_path = self.project_root + "/templates/style.css"

        self._export_size = (1920, 1080)

        self._save_path = str(self.project_root) + "/output/"

    def save_path(self) -> str:
        return self._save_path

    @property
    def css_path(self):
        return Path(self._read_css_path)

    def execute(self):
        htoi = Html2Image()
        htoi.output_path = self._save_path
        with open(self._read_html_path) as f:
            htoi.screenshot(
                f.read(),
                size=self._export_size,
                css_str=self.css_path.read_text(),
                save_as="output.png"
            )

