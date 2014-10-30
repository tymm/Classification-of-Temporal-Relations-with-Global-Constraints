from helper.nlp_persistence import Nlp_persistence
from helper.duration_cache import Duration_cache
from helper.strings_cache import Strings_cache
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from Result import Result
import cPickle as pickle

class System:
    def __init__(self, data, features=None):
        if features is not None:
            self.features = features
        else:
            self.features = []

        self.data = data

        self.training = None
        self.training_event_event = None
        self.training_event_timex = None

        self.test_event_event = None
        self.test_event_timex = None

        self.classifier = None

        self.y_predicted_event_event = None
        self.y_predicted_event_timex = None

    def create_features(self):
        nlp_persistence = None
        duration_cache = None
        strings_cache = None

        if "lemma" in self.features or "token" in self.features or "best" in self.features:
            strings_cache = Strings_cache()

        if "duration" in self.features or "duration_difference" in self.features or "best" in self.features:
            duration_cache = Duration_cache()

        if "dependency_types" in self.features or "dependency_is_root" in self.features or "duration" in self.features or "dependency_order" in self.features or "tense" in self.features or "aspect" in self.features or "lemma" in self.features or "best" in self.features:
            nlp_persistence = Nlp_persistence()
            print "Loading NLP data from file."
            nlp_persistence.load()
            print "Done loading NLP data from file."

        # Create training features and target values
        print "Creating features for the training data"

        # Set features
        self.data.training.pass_objects(self.features, strings_cache, nlp_persistence, duration_cache)

        X_train_event_event, y_train_event_event = self.data.training.get_event_event_feature_vectors_and_targets()
        X_train_event_timex, y_train_event_timex = self.data.training.get_event_timex_feature_vectors_and_targets()

        self.training_event_event = (X_train_event_event, y_train_event_event)
        self.training_event_timex = (X_train_event_timex, y_train_event_timex)

        print "Creating features for the test data"

        self.data.test.pass_objects(self.features, strings_cache, nlp_persistence, duration_cache)

        X_test_event_event, y_test_event_event = self.data.test.get_event_event_feature_vectors_and_targets()
        X_test_event_timex, y_test_event_timex = self.data.test.get_event_timex_feature_vectors_and_targets()

        self.test_event_event = (X_test_event_event, y_test_event_event)
        self.test_event_timex = (X_test_event_timex, y_test_event_timex)

        print "Done creating features"
        print

        # Close NLP cache and write new sentences to the cache
        if "dependency_types" in self.features or "dependency_is_root" in self.features or "dependency_order" in self.features or "tense" in self.features or "aspect" in self.features:
            nlp_persistence.close()

    def train(self):
        self.classifier_event_event = self._train_SVM(self.training_event_event)
        self.classifier_event_timex = self._train_SVM(self.training_event_timex)

    def save_classifiers(self):
        print "Saving classifiers to disk"
        with open("classifier_event_event.p", "wb") as f:
            pickle.dump(self.classifier_event_event, f, protocol=-1)

        with open("classifier_event_timex.p", "wb") as f:
            pickle.dump(self.classifier_event_timex, f, protocol=-1)

        print "Done"

    def eval(self):
        X_test_event_event = self.test_event_event[0]
        y_test_event_event = self.test_event_event[1]

        X_test_event_timex = self.test_event_timex[0]
        y_test_event_timex = self.test_event_timex[1]

        self.y_predicted_event_event = self.classifier_event_event.predict(X_test_event_event)
        self.y_predicted_event_timex = self.classifier_event_timex.predict(X_test_event_timex)

        result_event_event = Result(y_test_event_event, self.y_predicted_event_event)
        result_event_timex = Result(y_test_event_timex, self.y_predicted_event_timex)

        return (result_event_event, result_event_timex)

    def eval_global_model(self):
        """Needs apply_global_model() to be run before."""
        y_test_event_event = self.test_event_event[1]
        y_test_event_timex = self.test_event_timex[1]

        y_predicted_event_event_global_model = self.test_event_event_global_model_targets
        y_predicted_event_timex_global_model = self.test_event_timex_global_model_targets

        result_event_event = Result(y_test_event_event, y_predicted_event_event_global_model)
        result_event_timex = Result(y_test_event_timex, y_predicted_event_timex_global_model)

        return (result_event_event, result_event_timex)

    def create_confidence_scores(self):
        self.data.test.create_confidence_scores(self.classifier_event_event, self.classifier_event_timex)

    def apply_global_model(self):
        self.data.test.apply_global_model()
        self.test_event_event_global_model_targets = self.data.test.get_event_event_targets()
        self.test_event_timex_global_model_targets = self.data.test.get_event_timex_targets()

    def _train_random_forest(self, training_data):
        print "Train a random forest classifier"

        rf = RandomForestClassifier(n_jobs=2, n_estimators=5)
        rf.fit(training_data[0].toarray(), training_data[1])

        print "Done training the classifier."
        return rf

    def _train_naive_bayes(self, training_data):
        print "Train a naive bayes classifier"

        clf = MultinomialNB()
        clf.fit(training_data[0], training_data[1])

        print "Done training the classifier"
        return clf

    def _train_SVM(self, training_data):
        print "Train SVM"
        clf = svm.SVC(probability=True, kernel="poly", degree=2, C=1000, gamma=0.001, class_weight=None)

        clf.fit(training_data[0], training_data[1])

        print "Done training the classifier."
        return clf

    def use_tense(self):
        if not "tense" in self.features:
            self.features.append("tense")

    def use_same_tense(self):
        if not "same_tense" in self.features:
            self.features.append("same_tense")

    def use_aspect(self):
        if not "aspect" in self.features:
            self.features.append("aspect")

    def use_same_aspect(self):
        if not "same_aspect" in self.features:
            self.features.append("same_aspect")

    def use_dependency_is_root(self):
        if not "dependency_is_root" in self.features:
            self.features.append("dependency_is_root")

    def use_dependency_order(self):
        if not "dependency_order" in self.features:
            self.features.append("dependency_order")

    def use_dependency_type(self):
        if not "dependency_type" in self.features:
            self.features.append("dependency_type")

    def use_dct(self):
        if not "dct" in self.features:
            self.features.append("dct")

    def use_type(self):
        if not "type" in self.features:
            self.features.append("type")

    def use_polarity(self):
        if not "polarity" in self.features:
            self.features.append("polarity")

    def use_same_polarity(self):
        if not "same_polarity" in self.features:
            self.features.append("same_polarity")

    def use_class(self):
        if not "class" in self.features:
            self.features.append("class")

    def use_entity_distance(self):
        if not "entity_distance" in self.features:
            self.features.append("entity_distance")

    def use_sentence_distance(self):
        if not "sentence_distance" in self.features:
            self.features.append("sentence_distance")

    def use_textual_order(self):
        if not "textual_order" in self.features:
            self.features.append("textual_order")

    def use_duration(self):
        if not "duration" in self.features:
            self.features.append("duration")

    def use_duration_difference(self):
        if not "duration_difference" in self.features:
            self.features.append("duration_difference")

    def use_pos(self):
        if not "pos" in self.features:
            self.features.append("pos")

    def use_same_pos(self):
        if not "same_pos" in self.features:
            self.features.append("same_pos")

    def use_value(self):
        if not "value" in self.features:
            self.features.append("value")

    def use_temporal_signal(self):
        if not "temporal_signal" in self.features:
            self.features.append("temporal_signal")

    def use_lemma(self):
        if not "lemma" in self.features:
            self.features.append("lemma")

    def use_token(self):
        if not "token" in self.features:
            self.features.append("token")

    def use_all_features(self):
        if not "all" in self.features:
            self.features.append("all")

    def use_best_feature_set(self):
        self.features = ["best"]
