import os
from lxml import etree
from lxml.etree import tostring
from itertools import chain
from parsexml.text import Text
from parsexml.event import Event
import re

class Parser:
    def __init__(self, corpus_file):
        self.filename = corpus_file
        self.text_object = None
        self._parse(self.filename)

    def get_text_object(self):
        return self.text_object

    def _parse(self, filename):
        # Mapping xml data to python objects
        self.text_object = self._parse_xml_to_objects(filename)

    def _stringify_children(self, node):
        # Transfer sub tree into string
        text_with_tags = tostring(node)

        # Remove tags
        regex = re.compile(r"<.*?>")
        text = re.sub(r"<.*?>", "", text_with_tags)

        return text

    def _extract_text(self, xml_text_obj):
        text = self._stringify_children(xml_text_obj)
        return text

    def _create_event_objects(self, text, text_obj):
        for event in text.iterdescendants("EVENT"):
            event_obj = Event(event.get("eid"), text_obj, event.text)
            text_obj.append_event(event_obj)

        return text_obj

    def _create_relation_objects(self, root):
        """Must be called after _create_event_objects"""
        for relation in root.iterdescendants("TLINK"):
            lid = relation.get("lid")
            source_eid = relation.get("eventInstanceID")
            target_eid = relation.get("relatedToEventInstance")
            relation_type = relation.get("relType")

    def _parse_xml_to_objects(self, file):
        tree = etree.parse(file)
        root = tree.getroot()

        text = root.find("TEXT")

        extracted_text = self._extract_text(text)

        text_obj = Text(file, extracted_text)

        # Create Event objects and link them to the Text object
        self._create_event_objects(text, text_obj)

        # Create Relation objects and link them
        self._create_relation_objects(root)

        return text_obj


if __name__ == "__main__":
    a = Parser("data/training/TE3-Silver-data/AFP_ENG_19970401.0006.tml")
