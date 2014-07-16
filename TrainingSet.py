from Set import Set
from Feature import Feature

class TrainingSet(Set):
    def __init__(self, load=True, *corpora):
        Set.__init__(self, load, *corpora)

    def get_classification_data_event_event(self):
        X = []
        y = []

        for text_obj in self.text_objects:
            for relation in text_obj.relations:
                if relation.is_event_event():
                    f = Feature(relation)
                    #X.append(f.get_tense() + f.get_polarity() + f.get_same_tense() + f.get_same_aspect() + f.get_same_class() + f.get_same_pos() + f.get_textual_order() + f.get_sentence_distance())
                    feature = f.get_event_distance()

                    X.append(feature)
                    print feature
                    y.append(relation.get_result())

        return (X, y)
