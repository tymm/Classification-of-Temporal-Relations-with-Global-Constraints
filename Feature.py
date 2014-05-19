from feature.tense import Tense
from sklearn.preprocessing import OneHotEncoder

class Feature:
    def __init__(self, relation):
        self.relation = relation

    def get_tense(self):
        n_values = Tense.get_length()
        enc= OneHotEncoder(n_values=n_values, categorical_features=[0,1])
        enc.fit([n_values-1, n_values-1])

        tense = Tense(self.relation)

        feature = enc.transform([[tense.source, tense.target]]).toarray()[0]
        return feature
