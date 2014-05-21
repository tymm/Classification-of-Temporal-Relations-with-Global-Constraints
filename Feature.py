from feature.tense import Tense
from feature.same_tense import Same_tense
from feature.same_aspect import Same_aspect
from sklearn.preprocessing import OneHotEncoder

class Feature:
    def __init__(self, relation):
        self.relation = relation

    def get_tense(self):
        n_values = Tense.get_length()
        enc = OneHotEncoder(n_values=n_values, categorical_features=[0,1])
        enc.fit([n_values-1, n_values-1])

        tense = Tense(self.relation)

        feature = enc.transform([[tense.source, tense.target]]).toarray()[0]
        return feature

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
