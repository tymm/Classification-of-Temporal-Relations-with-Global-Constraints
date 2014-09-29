from Set import Set
from Feature import Feature
from feature.exception import FailedProcessingFeature

class TrainingSet(Set):
    def __init__(self, load=True, *corpora):
        Set.__init__(self, load, False, *corpora)

    def get_classification_data_event_event(self, features, lemma=None, token=None, nlp_persistence_obj=None):
        X = []
        y = []

        length = len(self._event_event_rels)

        features = self._remove_only_event_timex_features(features)

        for i, relation in enumerate(self._event_event_rels):
            try:
                f = Feature(relation, lemma, token, nlp_persistence_obj, features)
                feature = f.get_feature()
            except FailedProcessingFeature:
                continue

            relation.set_feature(feature)

            X.append(feature)
            y.append(relation.get_result())

            # Print progress
            self._print_progress(i, length)

        print
        return (X, y)

    def get_classification_data_event_timex(self, features, lemma=None, token=None, nlp_persistence_obj=None):
        X = []
        y = []

        length = len(self._event_timex_rels)

        features = self._remove_only_event_event_features(features)

        for i, relation in enumerate(self._event_timex_rels):
            try:
                f = Feature(relation, lemma, token, nlp_persistence_obj, features)
                feature = f.get_feature()
            except FailedProcessingFeature:
                continue

            relation.set_feature(feature)

            X.append(feature)
            y.append(relation.get_result())

            # Print progress
            self._print_progress(i, length)

        print
        return (X, y)
