import os
from parsexml.text import Text
from Persistence import Persistence
import sys
import multiprocessing
from helper.pickle_methods import activate

# Needs to be done in order to use multiprocessing
activate()

class Set(object):
    def __init__(self, load=True, test=False, *corpora):
        self.corpora = corpora
        self.load = load
        self.test = test
        # Hols all textfile objects
        self.text_objects = []
        self._parse()

        self._event_event_rels = []
        self._event_timex_rels = []

        self._extract_relations()

        self.relations = self._event_event_rels + self._event_timex_rels

    def _extract_relations(self):
        for text_obj in self.text_objects:
            for relation in text_obj.relations:
                if relation.is_event_event():
                    self._event_event_rels.append(relation)
                elif relation.is_event_timex():
                    self._event_timex_rels.append(relation)

    def _print_progress(self, position, length):
        sys.stdout.write("\r%d%%" % int(position*100/(length - 1)))
        sys.stdout.flush()

    def _parse(self):
        # Holds all corpora files
        files = []

        # Get all files
        for corpus in self.corpora:
            files = files + self._fetch_files(corpus)

        # Parse all files
        tmls = []
        for file in files:
            # Only parse *.tml files
            if not file.endswith('tml'):
                continue

            tmls.append(file)

        # Parse from files on all cores
        pool = multiprocessing.Pool()
        pool.map_async(self._parse_from_file, tmls, callback=self._append_text_obj)

        pool.close()
        pool.join()

    def _append_text_obj(self, text_obj):
        self.text_objects.append(text_obj)

    def _parse_from_file(self, file):
        # Mapping xml data to python objects
        text = Text(file, self.test)

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

    def _remove_only_event_event_features(self, features):
        features_event_timex = list(features)

        self._try_to_remove(features_event_timex, "same_tense")
        self._try_to_remove(features_event_timex, "same_aspect")
        self._try_to_remove(features_event_timex, "same_class")
        self._try_to_remove(features_event_timex, "same_pos")
        self._try_to_remove(features_event_timex, "same_polarity")
        self._try_to_remove(features_event_timex, "temporal_discourse")

        return features_event_timex

    def _remove_only_event_timex_features(self, features):
        features_event_event = list(features)

        self._try_to_remove(features_event_event, "dct")
        self._try_to_remove(features_event_event, "type")
        self._try_to_remove(features_event_event, "value")

        return features_event_event

    def _try_to_remove(self, l, value):
        try:
            l.remove(value)
        except ValueError:
            pass
