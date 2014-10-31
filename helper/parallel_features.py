import multiprocessing
from Feature import Feature
from feature.exception import FailedProcessingFeature
from multiprocessing import Value, Lock, Manager
from ctypes import c_int
import sys
import traceback

class Parallel_features(object):
    def __init__(self, text_objs, nlp_persistence_obj, strings_cache, duration_cache, features_event_event, features_event_timex):
        self.text_objs = text_objs
        self.processed_text_objs = []

        global nlp_persistence_obj_g
        # TODO: nlp_persistence_obj should not write stuff
        nlp_persistence_obj_g = nlp_persistence_obj

        global features_event_event_g
        features_event_event_g = features_event_event

        global features_event_timex_g
        features_event_timex_g = features_event_timex

        global duration_cache_g
        duration_cache_g = duration_cache

        global strings_cache_g
        strings_cache_g = strings_cache

        global _length
        _length = len(self.text_objs)

        global _counter
        global _counter_lock

        _counter = Value(c_int)
        _counter_lock = Lock()

        self._run()

    def _run(self):
        pool = multiprocessing.Pool()
        pool.map_async(self._get_feature, self.text_objs, callback=self._get_processed_text_objs)

        pool.close()
        pool.join()

    def _get_feature(self, text_obj):
        """Get feature data for a whole text object."""
        try:
            for relation in text_obj.relations:
                if relation.is_event_event():
                    f = Feature(relation, strings_cache_g, nlp_persistence_obj_g, duration_cache_g, features_event_event_g)
                    feature = f.get_feature()
                    relation.set_feature(feature)

                elif relation.is_event_timex():
                    f = Feature(relation, strings_cache_g, nlp_persistence_obj_g, duration_cache_g, features_event_timex_g)
                    feature = f.get_feature()
                    relation.set_feature(feature)

                # Append feature to relation in text_obj.relations_plain if existant
                if relation.is_event_event() or relation.is_event_timex():
                    if relation in text_obj.relations_plain:
                        # Search for relation
                        for rel in text_obj.relations_plain:
                            if rel == relation:
                                rel.set_feature(feature)
                                break

            # Print progress
            with _counter_lock:
                _counter.value += 1

                sys.stdout.write("\r%d%%" % int(_counter.value*100/(_length - 1)))
                sys.stdout.flush()

            return text_obj

        except Exception as e:
            # Print progress
            with _counter_lock:
                _counter.value += 1

                sys.stdout.write("\r%d%%" % int(_counter.value*100/(_length - 1)))
                sys.stdout.flush()

            print e
            print traceback.format_exc()

    def _get_processed_text_objs(self, text_objs):
        for text_obj in text_objs:
            self.processed_text_objs.append(text_obj)
