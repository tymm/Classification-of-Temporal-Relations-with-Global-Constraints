from Set import Set
from Feature import Feature
import numpy
from feature.exception import FailedProcessingFeature

class TestSet(Set):
    def __init__(self, *corpora):
        # No inverses and closures in the test set
        Set.__init__(self, False, False, *corpora)

    def create_evaluation_files(self):
        for text_obj in self.text_objects:
            text_obj.generate_output_tml_file()

    def _produce_predictions(self, relations, classifier):
        # Warning: It's way faster to do classifier.predict(features) instead of doing it for every relation at a time
        for relation in relations:
            predicted_class = classifier.predict(relation.feature)

            # Set the predicted class for the relation
            relation.predicted_class = predicted_class

    def _get_predicted_data(self, relations):
        y_predicted = []

        for relation in relations:
            y_predicted.append(relation.predicted_class)

        return y_predicted
