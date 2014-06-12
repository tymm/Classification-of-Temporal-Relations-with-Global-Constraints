from collections import OrderedDict
from parsexml.sentence import Sentence
from lxml import etree

class Text_structure:
    def __init__(self, filename, text_obj):
        self.filename = filename
        self.text_obj = text_obj
        # {Sentence: [Event, Timex, ...]
        self.structure = OrderedDict()

        self._entities_ordered = []
        self._entity_nodes_ordered = []

        self._build_entities_ordered()
        self._build_structure()

    def get_entities_ordered(self):
        return self._entities_ordered

    def get_structure(self):
        return self.structure

    def print_structure(self):
        print "----Structure start----"
        for sentence, entities in self.structure.items():
            print "---Sentence start---"
            print sentence.text
            for entity in entities:
                print entity.text

            print "---Sentence end---"
            print
        print "----Structure end----"
        print

    def get_sentence_distance(self, entity_one, entity_two):
        sentences = self.structure.values()

        position_one = None
        position_two = None

        for sentence in sentences:
            if entity_one in sentence or entity_two in sentence:
                # Start counting
                if entity_one in sentence and entity_two in sentence:
                    # Both entities are in the same sentence
                    return 0

                if entity_one in sentence:
                    position_one = sentences.index(sentence)

                if entity_two in sentence:
                    position_two = sentences.index(sentence)

        try:
            difference = abs(position_one - position_two)
        except TypeError:
            # One or both entities are not in any sentence
            difference = None

        return difference

    def _get_entity_by_node(self, entity_node):
        eid = entity_node.get("eid")

        if eid:
            # It's an event
            entity = self.text_obj.find_event_by_eid(eid)
        else:
            # It's a timex
            tid = entity_node.get("tid")
            entity = self.text_obj.find_timex_by_tid(tid)

        return entity

    def _build_entities_ordered(self):
        tree = etree.parse(self.filename)
        root_node = tree.getroot()

        text_node = root_node.find("TEXT")

        for entity_node in text_node:
            entity = self._get_entity_by_node(entity_node)

            self._entities_ordered.append(entity)
            self._entity_nodes_ordered.append(entity_node)

    def _build_structure(self):
        for entity_node in self._entity_nodes_ordered:
            sentence = Sentence(entity_node)
            # Get entity object by lxml object
            entity = self._get_entity_by_node(entity_node)

            # If sentence not yet in self.structure, we know that entity is the first entity of this sentence
            if sentence not in self.structure:
                self.structure.update({sentence: [entity]})
            # Sentence is already known. Let's append this entity to the already known sentence
            else:
                self.structure[sentence].append(entity)
