from parsexml.event import Event
import math

class Event_distance:
    """Number of entities between two entities.
    0 if adjacent.
    -1 if not in same sentence.
    Only measured when both entities are in the same sentence.
    """

    def __init__(self, relation):
        self.relation = relation
        self.text_structure = relation.parent.text_structure.structure

    def get_distance(self):
        entity_one = self.relation.source
        entity_two = self.relation.target

        start = None
        end = None
        for entities in self.text_structure.values():
            if entity_one in entities and entity_two in entities:
                start = entities.index(entity_one)
                end = entities.index(entity_two)

        if start and end:
            diff = abs(start-end)

            return diff-1
        else:
            return -1
