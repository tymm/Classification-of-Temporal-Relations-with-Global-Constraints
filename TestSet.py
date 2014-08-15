from Set import Set
from Feature import Feature
import numpy

class TestSet(Set):
    def __init__(self, load=True, *corpora):
        Set.__init__(self, load, *corpora)

    def classify_existing_event_event_relations(self, classifier, lemma=None, token=None):
        features = self._get_feature_data(self._event_event_rels, lemma, token)
        y_predicted = classifier.predict(features)
        y_truth = self._extract_classes(self._event_event_rels)

        return self._naive_evaluation(y_predicted, y_truth)

    def classify_existing_event_timex_relations(self, classifier, lemma=None, token=None):
        features = self._get_feature_data(self._event_timex_rels, lemma, token)
        y_predicted = classifier.predict(features)
        y_truth = self._extract_classes(self._event_timex_rels)

        return self._naive_evaluation(y_predicted, y_truth)

    def _get_feature_data(self, relations, lemma, token):
        features = []

        length = len(relations)

        for i, relation in enumerate(relations):
            f = Feature(relation, lemma, token)
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

