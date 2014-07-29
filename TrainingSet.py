from Set import Set
from Feature import Feature

class TrainingSet(Set):
    def __init__(self, load=True, *corpora):
        Set.__init__(self, load, *corpora)

    def get_classification_data_event_event(self, lemma, token):
        X = []
        y = []

        for text_obj in self.text_objects:
            for relation in text_obj.relations:
                if relation.is_event_event():
                    f = Feature(relation, lemma, token)
                    feature = f.get_feature()
                    relation.set_feature(feature)

                    X.append(feature)
                    y.append(relation.get_result())

        return (X, y)
