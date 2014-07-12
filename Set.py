import os
from Parser import Parser
from Feature import Feature
from Persistence import Persistence

class Set:
    def __init__(self, load=True, *corpora):
        self.corpora = corpora
        self.load = load
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
                    #X.append(f.get_tense() + f.get_polarity() + f.get_same_tense() + f.get_same_aspect() + f.get_same_class() + f.get_same_pos() + f.get_textual_order() + f.get_sentence_distance())
                    X.append(f.get_event_distance())
                    print f.get_event_distance()
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

            if self.load:
                # TODO: Loading and saving a huge dictionary like the one in the Persistance class takes a lot of time
                persistence = Persistence(file)

                # Lets try to load the parsed information from the persistence layer
                text_obj = persistence.get_text_object()

                if not text_obj:
                    # There is nothing stored yet, so lets parse from file
                    text_obj = self._parse_from_file(file)
                    # Save the parsed text object to the persitence layer
                    persistence.save(text_obj)

            else:
                # load=False, so let's parse from file
                text_obj = self._parse_from_file(file)
                # And save the parsed text object to the persitence layer

            self.text_objects.append(text_obj)

    def _parse_from_file(self, file):
        # Mapping xml data to python objects
        parser = Parser(file)
        parser.produce_relations()

        text_obj = parser.get_text_object()

        return text_obj

    def _fetch_files(self, directory):
        files = []

        # Append '/' if there is no at the end of directory string
        if not directory.endswith('/'):
            directory = directory + '/'

        for file in os.listdir(directory):
            files.append(directory + file)

        return files
