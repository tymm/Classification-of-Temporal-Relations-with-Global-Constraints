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
            entity = self._get_entity_by_node(entity_node)

            if sentence not in self.structure:
                self.structure.update({sentence: [entity]})

            self.structure[sentence].append(entity)
