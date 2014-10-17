from feature.tense import Tense
from feature.aspect import Aspect
from feature.same_tense import Same_tense
from feature.same_aspect import Same_aspect
from feature.same_class import Same_class
from feature.polarity import Polarity
from feature.pos import Pos
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
from feature.temporal_signal import Temporal_signal
from feature.event_class import Event_class
from feature.dct import Dct
from feature.type import Type
from feature.value import Value
from feature.token import Token
from feature.lemma import Lemma
import scipy
from scipy import sparse

class Feature(object):
    def __init__(self, relation, strings_cache, nlp_persistence_obj, duration_cache, features):
        self.relation = relation
        self.features = features
        self.duration_cache = duration_cache
        self.nlp_persistence_obj = nlp_persistence_obj
        self.strings_cache = strings_cache

    def _put_feature_into_sparse_matrix(self, func, flag_first, feature):
        if flag_first:
            feature = func()
            flag_first = False
        else:
            feature = sparse.hstack((feature, func()))

        return feature, flag_first

    def get_feature(self):
        feature = None
        flag_first = True

        if "all" in self.features:
            if self.relation.is_event_event():
                self.features = ["lemma", "token", "tense", "same_tense", "aspect", "same_aspect", "dependency_type", "dependency_order", "dependency_is_root", "class", "polarity", "same_polarity", "entity_distance", "sentence_distance", "textual_order", "pos", "same_pos", "duration", "duration_difference", "temporal_signal"]

            elif self.relation.is_event_timex():
                self.features = ["lemma", "token", "strings", "tense", "aspect", "dependency_type", "dependency_order", "type", "dependency_is_root", "dct", "polarity", "class", "entity_distance", "sentence_distance", "textual_order", "pos", "duration", "duration_difference", "value", "temporal_signal"]

        if "best" in self.features:
            if self.relation.is_event_event():
                self.features = ["lemma", "token", "tense", "same_tense", "aspect", "same_aspect", "dependency_type", "dependency_is_root", "polarity", "entity_distance", "sentence_distance", "textual_order", "pos", "same_pos", "duration_difference", "temporal_signal"]

            elif self.relation.is_event_timex():
                self.features = ["lemma", "token", "strings", "tense", "aspect", "dependency_type", "dct", "class", "entity_distance", "sentence_distance", "textual_order", "pos", "duration_difference", "temporal_signal"]

        if "lemma" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_lemma, flag_first, feature)

        if "token" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_token, flag_first, feature)

        if "tense" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_tense, flag_first, feature)

        if "same_tense" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_same_tense, flag_first, feature)

        if "aspect" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_aspect, flag_first, feature)

        if "same_aspect" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_same_aspect, flag_first, feature)

        if "dependency_type" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_dependency_type, flag_first, feature)

        if "dependency_order" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_dependency_order, flag_first, feature)

        if "dependency_is_root" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_dependency_is_root, flag_first, feature)

        if "dct" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_dct, flag_first, feature)

        if "polarity" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_polarity, flag_first, feature)

        if "same_polarity" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_same_polarity, flag_first, feature)

        if "class" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_event_class, flag_first, feature)

        if "type" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_type, flag_first, feature)

        if "entity_distance" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_entity_distance, flag_first, feature)

        if "sentence_distance" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_sentence_distance, flag_first, feature)

        if "textual_order" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_textual_order, flag_first, feature)

        if "pos" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_pos, flag_first, feature)

        if "same_pos" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_same_pos, flag_first, feature)

        if "duration" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_duration, flag_first, feature)

        if "duration_difference" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_duration_difference, flag_first, feature)

        if "value" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_value, flag_first, feature)

        if "temporal_signal" in self.features:
            feature, flag_first = self._put_feature_into_sparse_matrix(self.get_temporal_signal, flag_first, feature)

        return feature

    def get_dct(self):
        dct = Dct(self.relation)

        if dct.has_dct():
            return [0]
        else:
            return [1]

    def get_token(self):
        token = Token(self.relation, self.strings_cache)

        n_values = token.get_length()

        enc = OneHotEncoder(n_values=n_values, categorical_features=[0,1], dtype="int32")
        enc.fit([n_values-1, n_values-1])

        feature = enc.transform([[token.source, token.target]])
        return feature

    def get_lemma(self):
        lemma = Lemma(self.relation, self.strings_cache, self.nlp_persistence_obj)

        n_values = lemma.get_length()

        enc = OneHotEncoder(n_values=n_values, categorical_features=[0,1], dtype="int32")
        enc.fit([n_values-1, n_values-1])

        feature = enc.transform([[lemma.source, lemma.target]])
        return feature

    def get_value(self):
        value = Value(self.relation)
        n_values = value.get_length()

        enc = OneHotEncoder(n_values=n_values, categorical_features=[0,1], dtype="int32")
        enc.fit([n_values-1, n_values-1])

        feature = enc.transform([[value.source, value.target]]).toarray()[0]
        return feature.tolist()

    def get_temporal_signal(self):
        temporal_signal = Temporal_signal(self.relation)

        # First encode signal
        n_values = temporal_signal.get_length()
        signal = temporal_signal.get_signal()

        enc = OneHotEncoder(n_values=n_values, categorical_features=[0], dtype="int32")
        enc.fit([n_values-1])
        feature_signal = enc.transform([[signal]]).toarray()[0]
        feature_signal = feature_signal.tolist()

        # Encode if signal is at beginning of a sentence
        beginning = temporal_signal.is_signal_at_beginning()
        feature_beginning = None
        if beginning:
            feature_beginning = [0, 0, 1]
        elif beginning == False:
            feature_beginning = [0, 1, 0]
        elif beginning is None:
            feature_beginning = [1, 0, 0]

        # Encode the position of signal and e1 and signal and e2
        before_e1 = temporal_signal.entity_before_signal(self.relation.source)
        before_e2 = temporal_signal.entity_before_signal(self.relation.target)

        feature_order = None
        if before_e1 is None and before_e2 is None:
            feature_order = [0, 0, 0, 0, 1]
        elif before_e1 and before_e2:
            feature_order = [0, 0, 0, 1, 0]
        elif not before_e1 and not before_e2:
            feature_order = [0, 0, 1, 0, 0]
        elif before_e1 and not before_e2:
            feature_order = [0, 1, 0, 0, 0]
        elif not before_e1 and before_e2:
            feature_order = [1, 0, 0, 0, 0]

        return feature_signal + feature_beginning + feature_order

    def get_type(self):
        type = Type(self.relation)

        enc = OneHotEncoder(n_values=5, categorical_features=[0,1], dtype="int32")
        enc.fit([4,4])

        feature = enc.transform([[type.source, type.target]]).toarray()[0]
        return feature.tolist()

    def get_duration(self):
        duration = Duration(self.nlp_persistence_obj, self.duration_cache)

        n_values = duration.get_length()

        enc = OneHotEncoder(n_values=n_values, categorical_features=[0,1], dtype="int32")
        enc.fit([n_values-1, n_values-1])

        duration_source = duration.get_duration(self.relation.source)
        duration_target = duration.get_duration(self.relation.target)

        feature = enc.transform([[duration_source, duration_target]]).toarray()[0]
        return feature.tolist()

    def get_duration_difference(self):
        duration = Duration(self.nlp_persistence_obj, self.duration_cache)

        # Values: same, less, more, none
        n_values = 4

        enc = OneHotEncoder(n_values=n_values, categorical_features=[0], dtype="int32")
        enc.fit([n_values-1])

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

    def get_tense(self):
        n_values = Tense.get_length()
        enc = OneHotEncoder(n_values=n_values, categorical_features=[0,1], dtype="int32")
        enc.fit([n_values-1, n_values-1])

        tense = Tense(self.relation, self.nlp_persistence_obj)

        feature = enc.transform([[tense.source, tense.target]]).toarray()[0]
        return feature.tolist()

    def get_aspect(self):
        n_values = Aspect.get_length()
        enc = OneHotEncoder(n_values=n_values, categorical_features=[0,1], dtype="int32")
        enc.fit([n_values-1, n_values-1])

        aspect = Aspect(self.relation, self.nlp_persistence_obj)

        feature = enc.transform([[aspect.source, aspect.target]]).toarray()[0]
        return feature.tolist()

    def get_event_class(self):
        event_class = Event_class(self.relation)

        n_values = event_class.get_length()
        enc = OneHotEncoder(n_values=n_values, categorical_features=[0,1], dtype="int32")
        enc.fit([n_values-1, n_values-1])

        feature = enc.transform([[event_class.get_index_source(), event_class.get_index_target()]]).toarray()[0]
        return feature.tolist()

    def get_polarity(self):
        polarity = Polarity(self.relation)

        enc = OneHotEncoder(n_values=3, categorical_features=[0,1], dtype="int32")
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

    def get_pos(self):
        pos = Pos(self.relation, self.nlp_persistence_obj)
        n_values = pos.get_length()

        enc = OneHotEncoder(n_values=n_values, categorical_features=[0,1], dtype="int32")
        enc.fit([n_values-1, n_values-1])

        feature = enc.transform([[pos.source, pos.target]]).toarray()[0]
        return feature.tolist()

    def get_same_pos(self):
        same_pos = Same_pos(self.relation, self.nlp_persistence_obj)

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

        enc = OneHotEncoder(n_values=n_values+1, categorical_features=[0], dtype="int32")
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

        enc = OneHotEncoder(n_values=n_values, categorical_features=[0], dtype="int32")
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

        enc = OneHotEncoder(n_values=n_values, categorical_features=[0, 1], dtype="int32")
        enc.fit([n_values-1, n_values-1])

        feature = enc.transform([[value_source, value_target]]).toarray()[0]
        return feature.tolist()
