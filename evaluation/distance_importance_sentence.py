from Data import Data
from System import System
from parsexml.relation import Relation
from Result import Result

class Distance:
    def __init__(self):
        self.data = Data()
        self.system = System(self.data)

        system.use_all_features()
        system.use_feature_selection()

        self.system.create_features()
        self.system.train()
        self.system.save_predictions_to_relations()

        self.relations = self._get_relations()

        same_sentence, not_same_sentence = self._sort_relations_after_in_same_sentence()

        print "Same sentence event-event:"
        truth, predicted = self._get_truth_and_prediction(same_sentence)
        print Result(truth, predicted)

        print "Same sentence event-timex:"
        truth, predicted = self._get_truth_and_prediction(same_sentence, event_event=False)
        print Result(truth, predicted)

        print "Not same sentence event-event:"
        truth, predicted = self._get_truth_and_prediction(not_same_sentence)
        print Result(truth, predicted)

        print "Not same sentence event-timex:"
        truth, predicted = self._get_truth_and_prediction(not_same_sentence, event_event=False)
        print Result(truth, predicted)

    def _get_truth_and_prediction(self, rels, event_event=True):
        prediction = []
        truth = []

        for rel in rels:
            if event_event and rel.is_event_event():
                prediction.append(rel.predicted_class)
                truth.append(rel.relation_type)
            elif not event_event and rel.is_event_timex():
                prediction.append(rel.predicted_class)
                truth.append(rel.relation_type)

        return truth, prediction

    def _get_relations(self):
        rels = []

        for text_obj in self.data.test.text_objects:
            for relation in text_obj.relations:
                if relation.is_event_event():
                    rels.append(relation)
                elif relation.is_event_timex():
                    rels.append(relation)

        return rels

    def _sort_relations_after_in_same_sentence(self):
        same_sentence = []
        not_same_sentence = []

        for rel in self.relations:
            if rel.source.sentence == rel.target.sentence:
                same_sentence.append(rel)
            else:
                not_same_sentence.append(rel)

        return (same_sentence, not_same_sentence)

if __name__ == "__main__":
    distance = Distance()
