from Set import Set
from Feature import Feature

class TrainingSet(Set):
    def __init__(self, load=True, *corpora):
        Set.__init__(self, load, *corpora)

    def get_classification_data_event_event(self, lemma, token):
        X = []
        y = []

        for relation in self._event_event_rels:
            f = Feature(relation, lemma, token)
            feature = f.get_feature()
            relation.set_feature(feature)

            X.append(feature)
            y.append(relation.get_result())

        return (X, y)

    def get_classification_data_event_timex(self, lemma, token):
        X = []
        y = []

        for relation in self._event_timex_rels:
            f = Feature(relation, lemma, token)
            feature = f.get_feature()
            relation.set_feature(feature)

            X.append(feature)
            y.append(relation.get_result())

        return (X, y)
