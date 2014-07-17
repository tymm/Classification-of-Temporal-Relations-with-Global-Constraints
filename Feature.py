from feature.tense import Tense
from feature.same_tense import Same_tense
from feature.same_aspect import Same_aspect
from feature.same_class import Same_class
from feature.polarity import Polarity
from feature.same_pos import Same_pos
from feature.textual_order import Textual_order
from feature.sentence_distance import Sentence_distance
from feature.event_distance import Event_distance
from sklearn.preprocessing import OneHotEncoder


class Feature:
    def __init__(self, relation):
        self.relation = relation

    def get_feature(self):
        return self.get_sentence_distance()

    def get_tense(self):
        n_values = Tense.get_length()
        enc = OneHotEncoder(n_values=n_values, categorical_features=[0,1])
        enc.fit([n_values-1, n_values-1])

        tense = Tense(self.relation)

        feature = enc.transform([[tense.source, tense.target]]).toarray()[0]
        return feature.tolist()

    def get_polarity(self):
        polarity = Polarity(self.relation)

        enc = OneHotEncoder(n_values=2, categorical_features=[0,1])
        enc.fit([1, 1])

        feature = enc.transform([[polarity.source, polarity.target]]).toarray()[0]
        return feature.tolist()

    def get_same_tense(self):
        same_tense = Same_tense(self.relation)

        if same_tense.is_same():
            return [1]
        else:
            return [0]

    def get_same_aspect(self):
        same_aspect = Same_aspect(self.relation)

        if same_aspect.is_same():
            return [1]
        else:
            return [0]

    def get_same_class(self):
        same_class = Same_class(self.relation)

        if same_class.is_same():
            return [1]
        else:
            return [0]

    def get_same_pos(self):
        same_pos = Same_pos(self.relation)

        if same_pos.is_same():
            return [1]
        else:
            return [0]

    def get_textual_order(self):
        textual_order = Textual_order(self.relation)

        if textual_order.a_before_b():
            return [1]
        else:
            return [0]

    def get_sentence_distance(self):
        sentence_distance = Sentence_distance(self.relation)

        distance = sentence_distance.get_distance()
        return [distance]

    def get_event_distance(self):
        event_distance = Event_distance(self.relation)

        distance = event_distance.get_distance()
        return [distance]
