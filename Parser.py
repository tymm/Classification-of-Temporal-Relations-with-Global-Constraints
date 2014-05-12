import os
from lxml import etree

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

    def _parse_xml_to_objects(self, file):
        tree = etree.parse(file)
        root = tree.getroot()

        for text in root.iterdescendants("TEXT"):
            for event in text.iterdescendants("EVENT"):
                print event.text



if __name__ == "__main__":
    a = Parser("data/training/TE3-Silver-data/", "data/training/TBAQ-cleaned/AQUAINT/", "data/training/TBAQ-cleaned/TimeBank/")
