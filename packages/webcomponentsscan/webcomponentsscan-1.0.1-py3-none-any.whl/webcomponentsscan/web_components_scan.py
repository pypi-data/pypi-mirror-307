import json
import os

from html.parser import HTMLParser
from typing import Any


class CustomHTMLParser(HTMLParser):
    def __init__(self, custom_tags: list[str]) -> None:
        super().__init__()
        self.custom_tags = custom_tags
        self.tag_locations: dict[str, tuple[int, int]] = {}

    def handle_starttag(self, tag: str, _: Any) -> None:
        if tag in self.custom_tags:
            lineno, col_offset = self.getpos()
            self.tag_locations[tag] = (lineno, col_offset)


class WebComponentsScan:
    @staticmethod
    def get_manifest_file(path: str) -> dict:
        file = open(path, 'r')
        if file is None:
            raise FileNotFoundError

        return json.load(file)

    def get_custom_element_tags(self, manifest_file_path: str) -> list[str]:
        manifest = self.get_manifest_file(manifest_file_path)

        declarations = []
        if 'modules' in manifest:
            for module in manifest['modules']:
                if 'declarations' in module:
                    declarations.extend(module['declarations'])

        tags = [
            declaration['tagName']
            for declaration in declarations
            if 'tagName' in declaration
        ]

        return tags

    @staticmethod
    def list_html_files(path: str) -> list[str]:
        file_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".html"):
                    file_list.append(os.path.join(root, file))

        return file_list

    @staticmethod
    def search_for_components_in_html_file(path: str, tags: list[str]) -> dict[str, list[str]]:
        file = open(path, 'r')
        if file is None:
            raise FileNotFoundError

        file_contents = file.read()
        parser = CustomHTMLParser(tags)
        parser.feed(file_contents)

        tag_locations = parser.tag_locations
        if not tag_locations:
            return dict()

        return {
            tag: [
                f'{path}:{location[0]}'
            ]
            for tag, location in tag_locations.items()
        }

    def scan_html(self, path: str, manifest: str) -> dict[str, list[str]]:
        file_list = self.list_html_files(path=path)

        found_tags: dict[str, list[str]] = {}
        for file in file_list:
            tags = self.search_for_components_in_html_file(path=file, tags=self.get_custom_element_tags(manifest))

            for tag, paths in tags.items():
                if tag in found_tags:
                    found_tags[tag].extend(paths)
                else:
                    found_tags[tag] = paths

        return found_tags
