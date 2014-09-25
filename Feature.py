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
from feature.dependency_root import Dependency_root
from feature.dependency_type import Dependency_type
from feature.dependency_order import Dependency_order
from feature.dependency import EntitiesNotInSameSentence
from feature.duration import Duration
from feature.event_class import Event_class
from feature.dct import Dct
from feature.type import Type
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

        if "same_aspect" in self.features:
            feature += self.get_same_aspect()

        if "dependency_type" in self.features:
            feature += self.get_dependency_type()

        if "dependency_order" in self.features:
            feature += self.get_dependency_order()

        if "dependency_is_root" in self.features:
            feature += self.get_dependency_is_root()

        if "dct" in self.features:
            feature += self.get_dct()

        if "polarity" in self.features:
            feature += self.get_polarity()

        if "same_polarity" in self.features:
            feature += self.get_same_polarity()

        if "class" in self.features:
            feature += self.get_event_class()

        if "entity_distance" in self.features:
            feature += self.get_entity_distance()

        if "sentence_distance" in self.features:
            feature += self.get_sentence_distance()

        return feature

    def get_dct(self):
        dct = Dct(self.relation)

        if dct.has_dct():
            return [0]
        else:
            return [1]

    def get_type(self):
        type = Type(self.relation)

        enc = OneHotEncoder(n_values=5, categorical_features=[0,1])
        enc.fit([4,4])

        feature = enc.transform([[type.source, type.target]]).toarray()[0]
        return feature.tolist()

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
        # Maximum distance is 75 and average distance is 2.23
        sentence_distance = Sentence_distance(self.relation)
        distance = sentence_distance.get_distance()

        if distance == 0:
            return [0,0,0,0,0,0,0,1]
        elif distance == 1:
            return [0,0,0,0,0,0,1,0]
        elif distance == 2:
            return [0,0,0,0,0,1,0,0]
        elif distance >= 3 and distance <= 5:
            return [0,0,0,0,1,0,0,0]
        elif distance >= 6 and distance <= 8:
            return [0,0,0,1,0,0,0,0]
        elif distance >= 9 and distance <= 15:
            return [0,0,1,0,0,0,0,0]
        elif distance >= 15 and distance <= 20:
            return [0,1,0,0,0,0,0,0]
        elif distance > 20:
            return [1,0,0,0,0,0,0,0]

    def get_entity_distance(self):
        entity_distance = Entity_distance(self.relation)

        distance = entity_distance.get_distance()
        # Average distance in data is 0.67 and maximum distance is 10
        if distance == -1:
            return [0,0,0,0,0,0,1]
        elif distance == 0:
            return [0,0,0,0,0,1,0]
        elif distance == 1:
            return [0,0,0,0,1,0,0]
        elif distance == 2:
            return [0,0,0,1,0,0,0]
        elif distance == 3:
            return [0,0,1,0,0,0,0]
        elif distance == 4:
            return [0,1,0,0,0,0,0]
        elif distance > 4:
            return [1,0,0,0,0,0,0]

    def get_dependency_type(self):
        dependency_type = Dependency_type(self.relation, self.nlp_persistence_obj)

        n_values = dependency_type.get_length()

        enc = OneHotEncoder(n_values=n_values+1, categorical_features=[0])
        enc.fit([n_values])

        try:
            value = dependency_type.get_dependency_type()
        except EntitiesNotInSameSentence:
            value = n_values

        feature = enc.transform([[value]]).toarray()[0]
        return feature.tolist()

    def get_dependency_order(self):
        dependency_order = Dependency_order(self.relation, self.nlp_persistence_obj)

        # 0: Governor after Dependent, 1: Governor before Dependent, 2: Governor == Dependent, None: Entities not in same sentence
        n_values = 4

        enc = OneHotEncoder(n_values=n_values, categorical_features=[0])
        enc.fit([n_values-1])

        try:
            value = dependency_order.get_dependency_order()
        except EntitiesNotInSameSentence:
            value = 3

        feature = enc.transform([[value]]).toarray()[0]
        return feature.tolist()

    def get_dependency_is_root(self):
        # Describes whether either the source or target entity is root or not
        dependency_root = Dependency_root(self.relation, self.nlp_persistence_obj)

        try:
            dependency_root.get_dependency_is_root()
            value_source = dependency_root.value_source
            value_target = dependency_root.value_target
        except EntitiesNotInSameSentence:
            value_source = 2
            value_target = 2

        if value_source is None:
            print "Root is None."
            print self.relation.filename
            print self.relation.parent.relations.index(self.relation)

        n_values = 3

        enc = OneHotEncoder(n_values=n_values, categorical_features=[0, 1])
        enc.fit([n_values-1, n_values-1])

        feature = enc.transform([[value_source, value_target]]).toarray()[0]
        return feature.tolist()
