import os
from Parser import Parser
from Feature import Feature

class Set:
    def __init__(self, *corpora):
        self.corpora = corpora
        # Hols all textfile objects
        self.text_objects = []
        self._parse()

    def get_classification_data_event_event(self):
        X = []
        y = []

        for text_obj in self.text_objects:
            for relation in text_obj.relations:
                if relation.is_event_event():
                    f = Feature(relation)
                    X.append(f.get_tense() + f.get_same_tense() + f.get_same_aspect() + f.get_same_polarity() + f.get_same_class())
                    y.append(relation.get_result())

        return (X, y)

    def _parse(self):
        # Holds all corpora files
        files = []

        # Get all files
        for corpus in self.corpora:
            files = files + self._fetch_files(corpus)

        # Parse all files
        for file in files:
            # Only parse *.tml files
            if not file.endswith('tml'):
                continue

            # Mapping xml data to python objects
            parser = Parser(file)
            parser.produce_inverse_relations()
            # parser.produce_closure_relations()

            self.text_objects.append(parser.get_text_object())

    def _fetch_files(self, directory):
        files = []

        # Append '/' if there is no at the end of directory string
        if not directory.endswith('/'):
            directory = directory + '/'

        for file in os.listdir(directory):
            files.append(directory + file)

        return files
