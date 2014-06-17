from parsexml.event import Event

class Sentence_distance:
    def __init__(self, relation):
        self.relation = relation
        self.text_structure = relation.parent.text_structure

    def get_distance(self):
        entity_one = self.relation.source
        entity_two = self.relation.target

        # Detect the case that we have two entities which represent the same entity in the text
        if self._is_same_entity_in_text(entity_one, entity_two):
            # They are obviously in the same sentence
            return 0

        return self.text_structure.get_sentence_distance(entity_one, entity_two)

    def _is_same_entity_in_text(self, entity_one, entity_two):
        # The problem of having two entities which represent the same entity in the text apparently only happens for events
        if type(entity_one) == Event and type(entity_two) == Event:
            if entity_one.eid == entity_two.eid:
                return True

        return False


