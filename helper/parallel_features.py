import multiprocessing
from Feature import Feature
from feature.exception import FailedProcessingFeature

class Parallel_features(object):
    def __init__(self, text_objs, event_event=None, event_timex=None):
        self.text_objs = text_objs
        self.event_event = event_event
        self.event_timex = event_timex

        self.X = []
        self.y = []
        self.feature_data = (self.X, self.y)

        self._run()

    def _run(self):
        args = [(text_obj, None, None, None, ['dct']) for text_obj in self.text_objs]
        chunker = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]

        # Split into junks of 5 elements
        for chunk in chunker(args, 5):
            pool = multiprocessing.Pool()
            pool.map_async(self._get_feature, chunk, callback=self._get_feature_data)

            pool.close()
            pool.join()
            print "Done first batch"

    def _get_feature(self, args):
        try:
            text_obj, lemma, token, nlp_persistence_obj, features = args

            relations = []

            for relation in text_obj.relations:
                if self.event_event and relation.is_event_event():
                    try:
                        f = Feature(relation, lemma, token, nlp_persistence_obj, features)
                        feature = f.get_feature()
                        relation.set_feature(feature)
                    except FailedProcessingFeature:
                        continue

                elif self.event_timex and relation.is_event_timex():
                    try:
                        f = Feature(relation, lemma, token, nlp_persistence_obj, features)
                        feature = f.get_feature()
                        relation.set_feature(feature)
                    except FailedProcessingFeature:
                        continue

                relations.append(relation)

            return relations
        except Exception as e:
            print e

    def _get_feature_data(self, relations):
        for relation in relations:
            self.X.append(relation.feature)
            self.y.append(relation.relation_type)
