import multiprocessing
from Feature import Feature
from feature.exception import FailedProcessingFeature
from multiprocessing import Value, Lock, Manager
from ctypes import c_int
import sys
import traceback

class Parallel_features(object):
    def __init__(self, text_objs, nlp_persistence_obj, strings_cache, duration_cache, features, event_event=None, event_timex=None):
        self.features = features
        self.text_objs = text_objs
        self.nlp_persistence_obj = nlp_persistence_obj
        self.strings_cache = strings_cache
        self.duration_cache = duration_cache
        self.event_event = event_event
        self.event_timex = event_timex

        global nlp_persistence_obj_g
        # TODO: nlp_persistence_obj should not write stuff
        nlp_persistence_obj_g = self.nlp_persistence_obj

        global features_g
        features_g = self.features

        global duration_cache_g
        duration_cache_g = self.duration_cache

        global strings_cache_g
        strings_cache_g = self.strings_cache

        global event_event_g
        if event_event:
            event_event_g = True
        else:
            event_event_g = False

        if event_timex:
            event_event_g = False
        else:
            event_event_g = True

        global _length
        _length = len(self.text_objs)

        global _counter
        global _counter_lock

        _counter = Value(c_int)
        _counter_lock = Lock()

        self.X = []
        self.y = []
        self.feature_data = (self.X, self.y)

        self._run()

    def _run(self):
        pool = multiprocessing.Pool()
        pool.map_async(self._get_feature, self.text_objs, callback=self._get_feature_data)

        pool.close()
        pool.join()

    def _get_feature(self, text_obj):
        try:
            relations = []
            for relation in text_obj.relations:
                if event_event_g and relation.is_event_event():
                    f = Feature(relation, strings_cache_g, nlp_persistence_obj_g, duration_cache_g, features_g)
                    feature = f.get_feature()
                    relation.set_feature(feature)
                    relations.append(relation)

                elif not event_event_g and relation.is_event_timex():
                    f = Feature(relation, strings_cache_g, nlp_persistence_obj_g, duration_cache_g, features_g)
                    feature = f.get_feature()
                    relation.set_feature(feature)
                    relations.append(relation)

            # Print progress
            with _counter_lock:
                _counter.value += 1

                sys.stdout.write("\r%d%%" % int(_counter.value*100/(_length - 1)))
                sys.stdout.flush()

            return relations
        except Exception as e:
            # Print progress
            with _counter_lock:
                _counter.value += 1

                sys.stdout.write("\r%d%%" % int(_counter.value*100/(_length - 1)))
                sys.stdout.flush()

            print e
            print traceback.format_exc()

    def _get_feature_data(self, set_of_relations):
        for relations in set_of_relations:
            for relation in relations:
                self.X.append(relation.feature)
                self.y.append(relation.relation_type)
