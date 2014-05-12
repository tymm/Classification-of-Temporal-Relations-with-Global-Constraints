import os
from lxml import etree
from lxml.etree import tostring
from itertools import chain
from parsexml.text import Text
import re

class Parser:
    def __init__(self, *corpora):
        self.corpora = corpora
        # Hols all textfile objects
        self.text_objects = []
        self._parse(self.corpora)

    def _parse(self, corpora):
        # Holds all corpora files
        files = []

        # Get all files
        for corpus in corpora:
            files = files + self._fetch_files(corpus)

        # Parse all files
        for file in files:
            # Mapping xml data to python objects
            self.text_objects.append(self._parse_xml_to_objects(file))

    def _fetch_files(self, directory):
        files = []

        # Append '/' if there is no at the end of directory string
        if not directory.endswith('/'):
            directory = directory + '/'

        for file in os.listdir(directory):
            files.append(directory + file)

        return files

    def _stringify_children(self, node):
        # Transfer sub tree into string
        text_with_tags = tostring(node)

        # Remove tags
        regex = re.compile(r"<.*?>")
        text = re.sub(r"<.*?>", "", text_with_tags)

        return text

    def _extract_text(self, xml_text_obj):
        text = self._stringify_children(xml_text_obj)
        return text

    def _parse_xml_to_objects(self, file):
        tree = etree.parse(file)
        root = tree.getroot()

        text = root.find("TEXT")

        extracted_text = self._extract_text(text)

        for event in text.iterdescendants("EVENT"):
            print event.text


if __name__ == "__main__":
    a = Parser("data/training/TE3-Silver-data/", "data/training/TBAQ-cleaned/AQUAINT/", "data/training/TBAQ-cleaned/TimeBank/")
