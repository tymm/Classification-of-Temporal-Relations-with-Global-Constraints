from Set import Set
from Feature import Feature
import numpy
from feature.exception import FailedProcessingFeature

class TestSet(Set):
    def __init__(self, load=True, *corpora):
        Set.__init__(self, load, True, *corpora)

    def get_classification_data_event_event(self, features, lemma=None, token=None, nlp_persistence_obj=None):
        features = self._remove_only_event_timex_features(features)

        X, y = self._get_feature_data(self._event_event_rels, lemma, token, nlp_persistence_obj, features)

        return (X, y)

    def get_classification_data_event_timex(self, features, lemma=None, token=None, nlp_persistence_obj=None):
        features = self._remove_only_event_event_features(features)

        X, y = self._get_feature_data(self._event_timex_rels, lemma, token, nlp_persistence_obj, features)

        return (X, y)

    def create_evaluation_files(self):
        for text_obj in self.text_objects:
            text_obj.generate_output_tml_file()

    def _produce_predictions(self, relations, classifier):
        # Warning: It's way faster to do classifier.predict(features) instead of doing it for every relation at a time
        for relation in relations:
            predicted_class = classifier.predict(relation.feature)

            # Set the predicted class for the relation
            relation.predicted_class = predicted_class

    def _get_predicted_data(self, relations):
        y_predicted = []

        for relation in relations:
            y_predicted.append(relation.predicted_class)

        return y_predicted

    def _get_feature_data(self, relations, lemma, token, nlp_persistence_obj, features):
        X = []
        y = []

        length = len(relations)

        for i, relation in enumerate(relations):
            try:
                f = Feature(relation, lemma, token, nlp_persistence_obj, features)
                feature = f.get_feature()
            except FailedProcessingFeature:
                continue

            relation.set_feature(feature)

            X.append(feature)
            y.append(relation.relation_type)

            # Print progress
            self._print_progress(i, length)

        print
        return (X, y)
