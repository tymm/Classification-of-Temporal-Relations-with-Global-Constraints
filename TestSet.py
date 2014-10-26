from Set import Set
from Feature import Feature
import numpy
from feature.exception import FailedProcessingFeature

class TestSet(Set):
    def __init__(self, *corpora):
        # No inverses and closures in the test set
        Set.__init__(self, False, False, *corpora)
        self.relations_optimized = []

    def create_evaluation_files(self):
        for text_obj in self.text_objects:
            text_obj.generate_output_tml_file()

    def create_confidence_scores(self, classifier_event_event, classifier_event_timex):
        # Apply the global constraints to all relations of each text object
        for text_obj in self.text_objects:
            # Create all confidence scores between every relation
            text_obj.create_confidence_scores(classifier_event_event, classifier_event_timex)

    def apply_global_model(self):
        for text_obj in self.text_objects:
            # Create all optimal relations fpr text object
            ilp = Constraints(text_obj)
            self.relations_optimized += ilp.get_best_set()

    def get_event_event_targets(self):
        targets = []
        for relation in self.relations_optimized:
            if relation.is_event_event():
                targets.append(relation.relation_type)

        return targets

    def get_event_timex_targets(self):
        targets = []
        for relation in self.relations_optimized:
            if relation.is_event_timex():
                targets.append(relation.relation_type)

        return targets
