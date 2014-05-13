import os
from lxml import etree
from lxml.etree import tostring
from itertools import chain
from parsexml.text import Text
from parsexml.event import Event
from parsexml.relation import Relation
from parsexml.relationtype import RelationType
import re

class Parser:
    def __init__(self, corpus_file):
        self.filename = corpus_file
        self.text_obj = Text(self.filename)
        self._parse(self.filename)

    def get_text_object(self):
        return self.text_obj

    def _parse(self, filename):
        """Mapping xml data to python objects."""
        tree = etree.parse(filename)
        root_node = tree.getroot()

        text_node = root_node.find("TEXT")

        # Get text and pass it to Text object
        extracted_text = self._extract_text(text_node)
        self.text_obj.set_text(extracted_text)

        # Create Event objects and link them to the Text object
        self._create_event_objects(text_node, root_node)

        # Create Relation objects and link them
        self._create_relation_objects(root_node)

    def _stringify_children(self, node):
        # Transfer sub tree into string
        text_with_tags = tostring(node)

        # Remove tags
        regex = re.compile(r"<.*?>")
        text = re.sub(r"<.*?>", "", text_with_tags)

        return text

    def _extract_text(self, node):
        text = self._stringify_children(node)
        return text

    def _create_event_objects(self, text_node, root_node):
        for event in text_node.iterdescendants("EVENT"):
            eid = event.get("eid")
            eiid = None

            # Get eeid for event
            for instance in root_node.iterdescendants("MAKEINSTANCE"):
                instance_eid = instance.get("eventID")
                if instance_eid == eid:
                    eiid = instance.get("eiid")
                    break

            # Create Event object and append it to Text object
            event_obj = Event(eid, eiid, self.text_obj, event.text)
            self.text_obj.append_event(event_obj)

    def _create_relation_objects(self, root_node):
        """Must be called after _create_event_objects."""
        for relation in root_node.iterdescendants("TLINK"):
            lid = relation.get("lid")
            source_eiid = relation.get("eventInstanceID")
            target_eiid = relation.get("relatedToEventInstance")
            relation_type = relation.get("relType")

            # Get relation_type_id
            relation_type_id = RelationType.get_id(relation_type)

            # Find source event
            source_event_obj = self._find_event_by_eiid(source_eiid)

            # Find target event
            target_event_obj = self._find_event_by_eiid(target_eiid)

            relation_obj = Relation(lid, self.text_obj, source_event_obj, target_event_obj, relation_type_id)
            self.text_obj.append_relation(relation_obj)

    def _find_event_by_eiid(self, eiid):
        return self.text_obj.find_event_by_eiid(eiid)


if __name__ == "__main__":
    a = Parser("data/training/TE3-Silver-data/AFP_ENG_19970401.0006.tml")
