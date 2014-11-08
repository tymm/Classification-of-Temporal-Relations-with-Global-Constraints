from Data import Data
from System import System
import cPickle as pickle

class Contribution:
    def __init__(self):
        self.features_event_event = [["lemma", "token"], ["pos", "same_pos"], ["textual_order", "sentence_distance", "entity_distance"], "tense", "aspect", "class", "polarity", "same_tense", "same_aspect", "same_class", "same_polarity", "dependency_type", "dependency_order", "dependency_is_root", "temporal_signal", "temporal_discourse", "duration"]
        self.features_event_timex = [["lemma", "token"], "pos", ["textual_order", "sentence_distance", "entity_distance"], "tense", "aspect", "class", "polarity", "dct", "type", "value", "dependency_type", "dependency_order", "dependency_is_root", "temporal_signal", "duration"]

        self.features_event_event_len = len(self.features_event_event)
        self.features_event_timex_len = len(self.features_event_timex)
        self.max_len = max(self.features_event_event_len, self.features_event_timex_len)

        self.accuracies_event_event = []
        self.accuracies_event_timex = []

        self._run_systems()

    def save_accuracies(self):
        # save accuracies to file
        pickle.dump((self.accuracies_event_event, self.accuracies_event_timex), open("eval_contribution.p", "wb"))

    def _run_systems(self):
        for k in range(1, self.max_len+1):
            features = list(set(self._feature_series(k, self.features_event_event) + self._feature_series(k, self.features_event_timex)))
            print features

            data = Data()
            system = System(data, features)
            system.create_features()
            system.cross_validation()

            now = list(set(self._feature_series(k, self.features_event_event)))
            if k > 1:
                prev = list(set(self._feature_series(k-1, self.features_event_event)))

            if k > 1:
                if now != prev:
                    self.accuracies_event_event.append(system.crossval_accuracy_event_event)


            now = list(set(self._feature_series(k, self.features_event_timex)))
            if k > 1:
                prev = list(set(self._feature_series(k-1, self.features_event_timex)))
                print system.crossval_accuracy_event_event
            if k > 1:
                if now != prev:
                    self.accuracies_event_timex.append(system.crossval_accuracy_event_timex)
                    print system.crossval_accuracy_event_timex
            print

    def _feature_series(self, k, features_list):
        features = []

        for i, entry in enumerate(features_list):
            if i < k:
                if type(entry) == str:
                    features.append(entry)
                elif type(entry) == list:
                    features += entry
            else:
                break

        return features


if __name__ == "__main__":
    c = Contribution()
    c.save_accuracies()
