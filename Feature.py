from feature.tense import Tense
from feature.aspect import Aspect
from feature.same_tense import Same_tense
from feature.same_aspect import Same_aspect
from feature.same_class import Same_class
from feature.polarity import Polarity
from feature.same_pos import Same_pos
from feature.textual_order import Textual_order
from feature.sentence_distance import Sentence_distance
from feature.entity_distance import Entity_distance
from sklearn.preprocessing import OneHotEncoder
from feature.dependency import Dependency
from feature.duration import Duration
from feature.event_class import Event_class
import scipy

class Feature:
    def __init__(self, relation, lemmas, tokens, nlp_persistence_obj, features):
        self.relation = relation
        self.features = features
        self.nlp_persistence_obj = nlp_persistence_obj

        if "lemma" in self.features:
            self.lemmas = self.lemmas
        if "token" in self.features:
            self.tokens = tokens
        if "dependency" in self.features:
            self.dependency = Dependency(self.relation, nlp_persistence_obj)

    def get_feature(self):
        feature = []
        if "lemma" in self.features:
            feature += self.get_lemma()

        if "token" in self.features:
            feature += self.get_token()

        if "tense" in self.features:
            feature += self.get_tense()

        if "same_tense" in self.features:
            feature += self.get_same_tense()

        if "aspect" in self.features:
            feature += self.get_aspect()

        if "dependency_type" in self.features:
            feature += self.get_dependency_type()

        if "dependency_order" in self.features:
            feature += self.get_dependency_order()

        if "dependency_is_root" in self.features:
            feature += self.get_dependency_is_root()

        return feature

    def get_duration(self):
        duration = Duration()

        # +1 for NONE
        n_values = duration.get_length() + 1

        enc = OneHotEncoder(n_values=n_values, categorical_features=[0,1])
        enc.fit([n_values-1, n_values-1])

        # TODO: If entity is noun, use governing verb instead of noun here
        duration_source = duration.get_duration(self.relation.source)
        if duration_source is None:
            duration_source = n_values - 1

        duration_target = duration.get_duration(self.relation.target)
        if duration_target is None:
            duration_target = n_values - 1

        feature = enc.transform([[duration_source, duration_target]]).toarray()[0]
        return feature.tolist()

    def get_duration_difference(self):
        duration = Duration()

        # Values: same, less, more, none
        n_values = 4

        enc = OneHotEncoder(n_values=n_values, categorical_features=[0])
        enc.fit([n_values-1])

        # TODO: If entity is noun, use governing verb instead of noun here
        duration_source = duration.get_duration(self.relation.source)
        duration_target = duration.get_duration(self.relation.target)

        if duration_source is None or duration_target is None:
            feature = enc.transform([[3]]).toarray()[0]
            return feature.tolist()
        elif duration_source == duration_target:
            feature = enc.transform([[2]]).toarray()[0]
            return feature.tolist()
        elif duration_source < duration_target:
            feature = enc.transform([[1]]).toarray()[0]
            return feature.tolist()
        elif duration_source > duration_target:
            feature = enc.transform([[0]]).toarray()[0]
            return feature.tolist()

    def get_token(self):
        n_values = self.tokens.get_length()
        # +1 for the unkown value when the token is not known
        enc = OneHotEncoder(n_values=n_values+1, categorical_features=[0,1])
        enc.fit([n_values, n_values])

        source_index = self.tokens.get_index(self.relation.source.text)
        target_index = self.tokens.get_index(self.relation.target.text)

        # If the token is unknown, set the index to n_values as the "unknown" value
        if not source_index:
            source_index = n_values
        if not target_index:
            target_index = n_values

        feature = enc.transform([[source_index, target_index]]).toarray()[0]
        return feature.tolist()

    def get_lemma(self):
        n_values = self.lemmas.get_length()
        # +1 for the unkown value when the lemma is not known
        enc = OneHotEncoder(n_values=n_values+1, categorical_features=[0,1])
        enc.fit([n_values, n_values])

        source_index = self.lemmas.get_index(self.relation.source.text)
        target_index = self.lemmas.get_index(self.relation.target.text)

        # If the lemma is unknown, set the index to n_values as the "unknown" value
        if not source_index:
            source_index = n_values
        if not target_index:
            target_index = n_values

        feature = enc.transform([[source_index, target_index]]).toarray()[0]
        return feature.tolist()

    def get_tense(self):
        n_values = Tense.get_length()
        enc = OneHotEncoder(n_values=n_values, categorical_features=[0,1])
        enc.fit([n_values-1, n_values-1])

        tense = Tense(self.relation, self.nlp_persistence_obj)

        feature = enc.transform([[tense.source, tense.target]]).toarray()[0]
        return feature.tolist()

    def get_aspect(self):
        n_values = Aspect.get_length()
        enc = OneHotEncoder(n_values=n_values, categorical_features=[0,1])
        enc.fit([n_values-1, n_values-1])

        aspect = Aspect(self.relation, self.nlp_persistence_obj)

        feature = enc.transform([[aspect.source, aspect.target]]).toarray()[0]
        return feature.tolist()

    def get_event_class(self):
        event_class = Event_class(self.relation)

        n_values = event_class.get_length()
        enc = OneHotEncoder(n_values=n_values, categorical_features=[0,1])
        enc.fit([n_values-1, n_values-1])

        feature = enc.transform([[event_class.get_index_source(), event_class.get_index_target()]]).toarray()[0]
        return feature.tolist()

    def get_polarity(self):
        polarity = Polarity(self.relation)

        enc = OneHotEncoder(n_values=3, categorical_features=[0,1])
        enc.fit([2, 2])

        feature = enc.transform([[polarity.source, polarity.target]]).toarray()[0]
        return feature.tolist()

    def get_same_polarity(self):
        """This is an event-event only feature."""
        polarity = Polarity(self.relation)

        if polarity.target == polarity.source:
            return [0]
        else:
            return [1]

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
        # TODO: Make categoral
        return [distance]

    def get_entity_distance(self):
        entity_distance = Entity_distance(self.relation)

        distance = entity_distance.get_distance()
        # TODO: Make categoral
        return [distance]

    def get_dependency_type(self):
        n_values = len(self.dependency.dependency_types)

        enc = OneHotEncoder(n_values=n_values+1, categorical_features=[0])
        enc.fit([n_values])

        value = self.dependency.get_dependency_type()
        if value is None:
            value = n_values

        feature = enc.transform([[value]]).toarray()[0]
        return feature.tolist()

    def get_dependency_order(self):
        # 0: Governor after Dependent, 1: Governor before Dependent, 2: Governor at same position as Dependent, None: Entities not in same sentence
        n_values = 4

        enc = OneHotEncoder(n_values=n_values, categorical_features=[0])
        enc.fit([n_values-1])

        value = self.dependency.get_dependency_order()
        if not value:
            value = 3

        feature = enc.transform([[value]]).toarray()[0]
        return feature.tolist()

    def get_dependency_is_root(self):
        # Describes whether either the source or target entity is root or not
        is_source_root = self.dependency.is_source_root()
        is_target_root = self.dependency.is_target_root()

        if is_source_root is None:
            # The two entities are not in the same sentence
            value_source = 2
        elif is_source_root == True:
            value_source = 1
        elif is_source_root == False:
            value_source = 0

        if is_target_root is None:
            # The two entities are not in the same sentence
            value_target = 2
        elif is_target_root == True:
            value_target = 1
        elif is_target_root == False:
            value_target = 0

        n_values = 3

        enc = OneHotEncoder(n_values=n_values, categorical_features=[0, 1])
        enc.fit([n_values-1, n_values-1])

        feature = enc.transform([[value_source, value_target]]).toarray()[0]
        return feature.tolist()
