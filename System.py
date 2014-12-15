from helper.nlp_persistence import Nlp_persistence
from helper.duration_cache import Duration_cache
from helper.strings_cache import Strings_cache
from helper.discourse_cache import Discourse_cache
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from Result import Result
import cPickle as pickle
import numpy as np
from sklearn import cross_validation

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

        self.evaluation_accuracy_event_event = None
        self.evaluation_accuracy_event_timex = None

        self.crossval_accuracy_event_event = None
        self.crossval_accuracy_event_timex = None

    def create_features(self):
        nlp_persistence = None
        duration_cache = None
        strings_cache = None
        discourse_cache = None

        if "lemma" in self.features or "token" in self.features or "best" in self.features or "all" in self.features:
            strings_cache = Strings_cache()

        if "duration" in self.features or "duration_difference" in self.features or "best" in self.features or "all" in self.features:
            duration_cache = Duration_cache()

        if "temporal_discourse" in self.features or "best" in self.features or "all" in self.features:
            discourse_cache = Discourse_cache()

        if "dependency_types" in self.features or "dependency_is_root" in self.features or "duration" in self.features or "dependency_order" in self.features or "tense" in self.features or "aspect" in self.features or "lemma" in self.features or "best" in self.features or "all" in self.features:
            nlp_persistence = Nlp_persistence()
            print "Loading NLP data from file."
            nlp_persistence.load()
            print "Done loading NLP data from file."

        # Create training features and target values
        print "Creating features for the training data"

        # Set features
        self.data.training.pass_objects(self.features, strings_cache, nlp_persistence, duration_cache, discourse_cache)

        X_train_event_event, y_train_event_event = self.data.training.get_event_event_feature_vectors_and_targets()
        X_train_event_timex, y_train_event_timex = self.data.training.get_event_timex_feature_vectors_and_targets()

        self.training_event_event = (X_train_event_event, y_train_event_event)
        self.training_event_timex = (X_train_event_timex, y_train_event_timex)

        print "Creating features for the test data"

        self.data.test.pass_objects(self.features, strings_cache, nlp_persistence, duration_cache, discourse_cache)

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
        self.classifier_event_event = self._train_SVM_event(self.training_event_event)
        self.classifier_event_timex = self._train_SVM_timex(self.training_event_timex)

    def save_classifiers(self):
        print "Saving classifiers to disk"
        with open("classifier_event_event.p", "wb") as f:
            pickle.dump(self.classifier_event_event, f, protocol=-1)

        with open("classifier_event_timex.p", "wb") as f:
            pickle.dump(self.classifier_event_timex, f, protocol=-1)

        print "Done"

    def eval(self, quiet=False):
        X_test_event_event = self.test_event_event[0]
        y_test_event_event = self.test_event_event[1]

        X_test_event_timex = self.test_event_timex[0]
        y_test_event_timex = self.test_event_timex[1]

        self.y_predicted_event_event = self.classifier_event_event.predict(X_test_event_event)
        self.y_predicted_event_timex = self.classifier_event_timex.predict(X_test_event_timex)

        result_event_event = Result(y_test_event_event, self.y_predicted_event_event)
        result_event_timex = Result(y_test_event_timex, self.y_predicted_event_timex)

        if quiet:
            self.evaluation_accuracy_event_event = result_event_event._get_accuracy_paper()
            self.evaluation_accuracy_event_timex = result_event_timex._get_accuracy_paper()
        else:
            return (result_event_event, result_event_timex)

    def cross_validation(self):
        X_event_event, y_event_event = self.training_event_event
        X_event_timex, y_event_timex = self.training_event_timex

        # Do this with the SVM classifier we found best via grid search
        clf_ee = svm.SVC(probability=True, kernel="poly", degree=2, C=1000, gamma=0.0, class_weight=None)
        clf_et = svm.SVC(probability=True, kernel="poly", degree=3, C=100, gamma=0.0, class_weight=None)

        kfold = cross_validation.KFold(len(y_event_event), n_folds=5)
        accs = cross_validation.cross_val_score(clf_ee, X_event_event, y_event_event, cv=kfold, n_jobs=-1)
        self.crossval_accuracy_event_event = np.mean(accs)

        kfold = cross_validation.KFold(len(y_event_timex), n_folds=5)
        accs = cross_validation.cross_val_score(clf_et, X_event_timex, y_event_timex, cv=kfold, n_jobs=-1)
        self.crossval_accuracy_event_timex = np.mean(accs)

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

    def save_predictions_to_relations(self):
        """self.train() must be called before."""
        for text_obj in self.data.test.text_objects:
            for relation in text_obj.relations:
                if relation.is_event_event():
                    relation.predicted_class = self.classifier_event_event.predict(relation.feature)
                elif relation.is_event_timex():
                    relation.predicted_class = self.classifier_event_timex.predict(relation.feature)

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

    def _train_SVM_event(self, training_data):
        print "Train SVM"
        clf = svm.SVC(probability=True, kernel="poly", degree=2, C=1000, gamma=0.0, class_weight=None)

        clf.fit(training_data[0], training_data[1])

        print "Done training the classifier."
        return clf

    def _train_SVM_timex(self, training_data):
        print "Train SVM"
        clf = svm.SVC(probability=True, kernel="poly", degree=3, C=100, gamma=0.0, class_weight=None)

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

    def use_feature_selection(self):
        """Only useful in combination with "all". Selects the features found best in recursive feature elimination."""
        if not "feature_selection" in self.features:
            self.features.append("feature_selection")

    def use_same_features_as_in_reference_paper(self):
        if not "best" in self.features:
            self.features.append("best")

    def use_best_feature_set(self):
        self.use_all_features()
