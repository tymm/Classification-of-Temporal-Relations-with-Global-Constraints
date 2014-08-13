from Set import Set
from Feature import Feature

class TrainingSet(Set):
    def __init__(self, load=True, *corpora):
        Set.__init__(self, load, *corpora)

    def get_classification_data_event_event(self, lemma=None, token=None):
        X = []
        y = []

        length = len(self._event_event_rels)

        for i, relation in enumerate(self._event_event_rels):
            f = Feature(relation, lemma, token)
            feature = f.get_feature()
            relation.set_feature(feature)

            X.append(feature)
            y.append(relation.get_result())

            # Print progress
            self._print_progress(i, length)

        print
        return (X, y)

    def get_classification_data_event_timex(self, lemma=None, token=None):
        X = []
        y = []

        length = len(self._event_timex_rels)

        for i, relation in enumerate(self._event_timex_rels):
            f = Feature(relation, lemma, token)
            feature = f.get_feature()
            relation.set_feature(feature)

            X.append(feature)
            y.append(relation.get_result())

            # Print progress
            self._print_progress(i, length)

        print
        return (X, y)
