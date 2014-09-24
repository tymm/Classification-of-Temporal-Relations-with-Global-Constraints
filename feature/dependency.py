import logging

class Dependency:
    def __init__(self, relation, nlp_persistence_obj):
        self.relation = relation
        self.source = relation.source
        self.target = relation.target

        self.nlp_persistence_obj = nlp_persistence_obj

        # These features only make sense when both entities are in the same sentence
        if self.relation.target.sentence == self.relation.source.sentence:
            self.sentence = self.relation.target.sentence
            self.tree = nlp_persistence_obj.get_info_for_sentence(self.sentence)

            # Get collapsed dependency relations
            self.collapsed_dependencies = self.nlp_persistence_obj.get_collapsed_dependencies(self.source.sentence)

    def _check_if_relation_is_in_same_sentence(self):
        if self.relation.target.sentence == self.relation.source.sentence:
            return True
        else:
            raise EntitiesNotInSameSentence

class EntitiesNotInSameSentence(Exception):
    def __str__(self):
        return repr("Both entities have to be in the same sentence for this feature.")
