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

        #X, y = self._get_feature_data(self._event_event_rels, lemma, token, nlp_persistence_obj, features)
        X, y = self._get_feature_data(lemma, token, nlp_persistence_obj, features, event_event=True)

        return (X, y)

    def get_classification_data_event_timex(self, features, lemma=None, token=None, nlp_persistence_obj=None):
        X = []
        y = []

        length = len(self._event_timex_rels)

        features = self._remove_only_event_event_features(features)

        X, y = self._get_feature_data(lemma, token, nlp_persistence_obj, features, event_timex=True)

        return (X, y)
