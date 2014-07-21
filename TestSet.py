from Set import Set
from Feature import Feature
import numpy

class TestSet(Set):
    def __init__(self, load=True, *corpora):
        Set.__init__(self, load, *corpora)

        self._ground_truth_events_X = []
        self._ground_truth_events_y = []
        self._set_ground_truth_data()

        # Deleting all relations because we don't need them since we create all possible relations anyway
        self._delete_all_exisiting_relations()
        # Creating all possible relations
        self._create_all_relations_and_features()

    def _delete_all_exisiting_relations(self):
        for text_obj in self.text_objects:
            text_obj.relations = []

    def _create_all_relations_and_features(self):
        """Creating all possible relations between all entities in all text objects of this set."""
        # Creating all possible relations and their features
        for text_obj in self.text_objects:
            text_obj.create_all_relations_and_features()

    def create_confidence_scores(self, classifier):
        """Must be called after self._create_all_relations_and_features()."""
        for text_obj in self.text_objects:
            for relation in text_obj.relations:
                confidence_score = self._get_proba_of_relation(classifier, relation)
                relation.confidence_score = confidence_score

    def _get_proba_of_relation(self, classifier, relation):
        _class = relation.get_result()
        index = numpy.where(classifier.classes_==_class)

        all_probas = classifier.predict_proba(relation.get_feature())
        try:
            # Return the probability of the class the relation has
            return all_probas[0][index][0]
        except IndexError:
            # There was no sample of this class in the training data
            # Return 0 as confidence score
            return 0.0

    def _set_ground_truth_data(self):
        for text_obj in self.text_objects:
            for relation in text_obj.relations:
                if relation.is_event_event():
                    self._ground_truth_events_X.append(relation)
                    self._ground_truth_events_y.append(relation.get_result())

    def find_best_set_of_relations(self):
        for text_obj in self.text_objects:
            # Passing all possible relations
            ilp = Constraints(text_obj.relations)
            # And getting back the best subset ('best' in tems of the model)
            best_set = ilp.return_best_subset()

            # Set the best set of relations as the relations of text_obj
            text_obj.relations = best_set

    def get_predicted_data(self):
        pass
