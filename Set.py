import os
from parsexml.text import Text
from Persistence import Persistence
import sys
import multiprocessing
from helper.pickle_methods import activate
from helper.parallel_features import Parallel_features
from feature.exception import FailedProcessingFeature
from Feature import Feature
from helper.sparse import build_sparse_matrix

# Needs to be done in order to use multiprocessing
activate()

class Set(object):
    def __init__(self, inverse=False, closure=False, *corpora):
        self.corpora = corpora
        self.inverse = inverse
        self.closure = closure

        # There are no features yet
        self._processed = False

        global inverse_g
        inverse_g = self.inverse

        global closure_g
        closure_g = self.closure

        # Hols all textfile objects
        self.text_objects = []
        self._parse()

        self._event_event_rels = []
        self._event_timex_rels = []

        self._extract_relations()

        self.relations = self._event_event_rels + self._event_timex_rels

        # The following needs to be passed with self.pass_objects()
        self.features = None
        self.strings_cache = None
        self.nlp_persistence_obj = None
        self.duration_cache = None

    def pass_objects(self, features, strings_cache, nlp_persistence_obj, duration_cache):
        """Needs to be called before self.get_event_{event,timex}_feature_vectors_and_target()."""
        self.features = features
        self.strings_cache = strings_cache
        self.nlp_persistence_obj = nlp_persistence_obj
        self.duration_cache = duration_cache

    def get_event_event_feature_vectors_and_targets(self):
        if not self._processed:
            self._get_feature_data()
            self._processed = True

        X = []
        y = []

        # self.text_objects include feature data now
        for text_obj in self.text_objects:
            for relation in text_obj.relations:
                if relation.is_event_event():
                    X.append(relation.feature)
                    y.append(relation.relation_type)

        sparse_X_matrix = build_sparse_matrix(X)
        return (sparse_X_matrix, y)

    def get_event_timex_feature_vectors_and_targets(self):
        if not self._processed:
            self._get_feature_data()
            self._processed = True

        X = []
        y = []

        # self.text_objects include feature data now
        for text_obj in self.text_objects:
            for relation in text_obj.relations:
                if relation.is_event_timex():
                    X.append(relation.feature)
                    y.append(relation.relation_type)

        sparse_X_matrix = build_sparse_matrix(X)
        return (sparse_X_matrix, y)

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
        from TestSet import TestSet
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
        if issubclass(self.__class__, TestSet):
            pool.map_async(self._parse_from_file_test, tmls, callback=self._append_text_objs)
        else:
            pool.map_async(self._parse_from_file_training, tmls, callback=self._append_text_objs)

        pool.close()
        pool.join()

    def _append_text_objs(self, text_objs):
        self.text_objects += text_objs

    def _parse_from_file_test(self, file):
        try:
            text = Text(file, inverse=inverse_g, closure=closure_g, only_basic=False)
            return text
        except Exception as e:
            print e

    def _parse_from_file_training(self, file):
        try:
            text = Text(file, inverse=inverse_g, closure=closure_g, only_basic=True)
            return text
        except Exception as e:
            print e

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

    def _get_feature_data(self):
        features_event_event = self._remove_only_event_timex_features(self.features)
        features_event_timex = self._remove_only_event_event_features(self.features)

        parallel_processing = Parallel_features(self.text_objects, self.nlp_persistence_obj, self.strings_cache, self.duration_cache, features_event_event, features_event_timex)
        text_objs_with_feature_data = parallel_processing.processed_text_objs

        self.text_objects = text_objs_with_feature_data

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

class WrongArguments(Exception):
    def __str__(self):
        return repr("Using wrong arguments.")
