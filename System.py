from helper.nlp_persistence import Nlp_persistence
from sklearn.ensemble import RandomForestClassifier
from Result import Result

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

        self.classifier = None

    def create_features(self):
        lemma = None
        token = None
        nlp_persistence = None

        if "lemma" in self.features:
            lemma = Lemma(training)
        if "token" in self.features:
            token = Token(training)
        if "dependency_types" in self.features or "dependency_is_root" in self.features or "dependency_order" in self.features or "tense" in self.features or "aspect" in self.features:
            nlp_persistence = Nlp_persistence()
            print "Loading NLP data from file."
            nlp_persistence.load()
            print "Done loading NLP data from file."

        # Create training features and target values
        print "Creating features for the training data"
        X_train_event_event, y_train_event_event = self.data.training.get_classification_data_event_event(self.features, lemma, token, nlp_persistence)
        X_train_event_timex, y_train_event_timex = self.data.training.get_classification_data_event_timex(self.features, lemma, token, nlp_persistence)

        self.training = (X_train_event_event + X_train_event_timex, y_train_event_event + y_train_event_timex)
        self.training_event_event = (X_train_event_event, y_train_event_event)
        self.training_event_timex = (X_train_event_timex, y_train_event_timex)

        print "Creating features for the test data"
        X_test_event_event, y_test_event_event = self.data.test.get_classification_data_event_event(self.features, lemma, token, nlp_persistence)
        X_test_event_timex, y_test_event_timex = self.data.test.get_classification_data_event_timex(self.features, lemma, token, nlp_persistence)

        self.test = (X_test_event_event + X_test_event_timex, y_test_event_event + y_test_event_timex)
        self.test_event_event = (X_test_event_event, y_test_event_event)
        self.test_event_timex = (X_test_event_timex, y_test_event_timex)

        print "Done creating features"
        print

        # Close NLP cache and write new sentences to the cache
        if "dependency_types" in self.features or "dependency_is_root" in self.features or "dependency_order" in self.features or "tense" in self.features or "aspect" in self.features:
            nlp_persistence.close()

    def train(self):
        # Load features before using train()
        if not self.training:
            self.create_features()

        #self.classifier = self._train_random_forest(self.training)
        self.classifier_event_event = self._train_random_forest(self.training_event_event)
        self.classifier_event_timex = self._train_random_forest(self.training_event_timex)

    def eval(self):
        # Train classifier before using test()
        if not self.classifier and not self.classifier_event_event and not self.classifier_event_timex:
            self.train()

        X_test_event_event = self.test_event_event[0]
        y_test_event_event = self.test_event_event[1]

        X_test_event_timex = self.test_event_timex[0]
        y_test_event_timex = self.test_event_timex[1]

        y_predicted_event_event = self.classifier_event_event.predict(X_test_event_event)
        y_predicted_event_timex = self.classifier_event_timex.predict(X_test_event_timex)

        result_event_event = Result(y_test_event_event, y_predicted_event_event)
        result_event_timex = Result(y_test_event_timex, y_predicted_event_timex)

        return (result_event_event, result_event_timex)

    def _train_random_forest(self, training_data):
        print "Train a random forest classifier"

        rf = RandomForestClassifier(n_jobs=2, n_estimators=5)
        rf.fit(training_data[0], training_data[1])

        print "Done training the classifier"
        return rf

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
