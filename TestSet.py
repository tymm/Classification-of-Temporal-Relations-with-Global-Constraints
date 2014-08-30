from Set import Set
from Feature import Feature
import numpy

class TestSet(Set):
    def __init__(self, load=True, *corpora):
        Set.__init__(self, load, *corpora)

    def classify_existing_event_event_relations(self, classifier, lemma=None, token=None, nlp_persistence_obj=None):
        features = self._get_feature_data(self._event_event_rels, lemma, token, nlp_persistence_obj)

        self._produce_predictions(self._event_event_rels, classifier)

        y_predicted = self._get_predicted_data(self._event_event_rels)
        y_truth = self._extract_classes(self._event_event_rels)

        return self._naive_evaluation(y_predicted, y_truth)

    def classify_existing_event_timex_relations(self, classifier, lemma=None, token=None, nlp_persistence_obj=None):
        features = self._get_feature_data(self._event_timex_rels, lemma, token, nlp_persistence_obj)

        self._produce_predictions(self._event_timex_rels, classifier)

        y_predicted = self._get_predicted_data(self._event_timex_rels)
        y_truth = self._extract_classes(self._event_timex_rels)

        return self._naive_evaluation(y_predicted, y_truth)

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

    def _get_feature_data(self, relations, lemma, token, nlp_persistence_obj):
        features = []

        length = len(relations)

        for i, relation in enumerate(relations):
            f = Feature(relation, lemma, token, nlp_persistence_obj)
            feature = f.get_feature()
            relation.set_feature(feature)

            features.append(feature)

            # Print progress
            self._print_progress(i, length)

        print
        return features

    def _extract_classes(self, relations):
        y = []

        for relation in relations:
            y.append(relation.get_result())

        return y

    def _naive_evaluation(self, predicted, truth):
        true_pos = 0

        for i, p in enumerate(predicted):
            if p == truth[i]:
                true_pos += 1

        return true_pos * 100 / len(predicted)
