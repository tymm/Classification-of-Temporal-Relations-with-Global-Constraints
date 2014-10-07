import multiprocessing
from Feature import Feature
from feature.exception import FailedProcessingFeature
from multiprocessing import Value, Lock, Manager
from ctypes import c_int
import sys

class Parallel_features(object):
    def __init__(self, text_objs, nlp_persistence_obj, duration_cache, features, event_event=None, event_timex=None):
        self.features = features
        self.text_objs = text_objs
        self.nlp_persistence_obj = nlp_persistence_obj
        self.duration_cache = duration_cache
        self.event_event = event_event
        self.event_timex = event_timex

        print "Creating manager stuff"
        self.manager = Manager()
        self.shared = self.manager.dict()
        self.shared["nlp"] = self.nlp_persistence_obj
        self.shared["duration"] = self.duration_cache
        self.shared["features"] = self.features
        if self.event_event:
            self.shared["event_event"] = True
        else:
            self.shared["event_event"] = False
        print "done manager"

        self._length = len(self.text_objs)
        #self._counter = Value(c_int)
        #self._counter_lock = Lock()

        self.X = []
        self.y = []
        self.feature_data = (self.X, self.y)

        self._run()

    def _run(self):
        args = [(arg, self.shared) for arg in self.text_objs]

        pool = multiprocessing.Pool()
        pool.map_async(self._get_feature, args, callback=self._get_feature_data)

        pool.close()
        pool.join()

    def _get_feature(self, args):
        try:
            text_obj, shared = args

            relations = []

            for relation in text_obj.relations:
                if shared["event_event"] and relation.is_event_event():
                    try:
                        f = Feature(relation, None, None, shared["nlp"], shared["duration"], shared["features"])
                        feature = f.get_feature()
                        print feature
                        relation.set_feature(feature)
                    except FailedProcessingFeature:
                        continue

                elif not shared["event_event"] and relation.is_event_timex():
                    try:
                        f = Feature(relation, None, None, shared["nlp"], shared["duration"], shared["features"])
                        feature = f.get_feature()
                        print feature
                        relation.set_feature(feature)
                    except FailedProcessingFeature:
                        continue

                relations.append(relation)

            #self._increment_and_print_progress()
            return relations
        except Exception as e:
            #self._increment_and_print_progress()
            print e

    def _increment_and_print_progress(self):
        with counter_lock:
            counter.value += 1

            sys.stdout.write("\r%d%%" % int(counter.value*100/(self._length - 1)))
            sys.stdout.flush()

    def _get_feature_data(self, set_of_relations):
        for relations in set_of_relations:
            for relation in relations:
                print relation.feature
                self.X.append(relation.feature)
                self.y.append(relation.relation_type)
