import os
from parsexml.text import Text
from Persistence import Persistence

class Set:
    def __init__(self, load=True, *corpora):
        self.corpora = corpora
        self.load = load
        # Hols all textfile objects
        self.text_objects = []
        self._parse()

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
        text = Text(file)

        return text

    def _fetch_files(self, directory_or_file):
        files = []

        if os.path.isfile(directory_or_file):
            # It's a file
            return [directory_or_file]
        else:
            # It's a directory

            # Append '/' if there is no at the end of directory string
            if not directory_or_file.endswith('/'):
                directory_or_file = directory_or_file + '/'

            for file in os.listdir(directory_or_file):
                files.append(directory_or_file + file)

            return files
