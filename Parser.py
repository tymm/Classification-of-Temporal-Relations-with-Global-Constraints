import os
from lxml import etree
from lxml.etree import tostring
from itertools import chain
from parsexml.text import Text
from parsexml.event import Event
from parsexml.relation import Relation
from parsexml.sentence import Sentence
from parsexml.timex import Timex
from parsexml.relationtype import RelationType
from helper.closure import Closure
import re

class Parser:
    def __init__(self, corpus_file):
        self.filename = corpus_file
        self.text_obj = Text(self.filename)
        self._parse(self.filename)
        # Build entity order for text_obj
        self.text_obj.build_text_structure()

    def get_text_object(self):
        return self.text_obj

    def get_relations(self):
        return self.text_obj.relations

    def _produce_closure_relations(self):
        # Create temporal closures for BEFORE
        closure = Closure(self.text_obj, RelationType.BEFORE)
        closure_relations_before = closure.get_closure_relations()
        self.text_obj.relations = self.text_obj.relations + closure_relations_before

        # Create temporal closures for AFTER
        closure = Closure(self.text_obj, RelationType.AFTER)
        closure_relations_before = closure.get_closure_relations()
        self.text_obj.relations = self.text_obj.relations + closure_relations_before

        # Create temporal closures for INCLUDES
        closure = Closure(self.text_obj, RelationType.INCLUDES)
        closure_relations_before = closure.get_closure_relations()
        self.text_obj.relations = self.text_obj.relations + closure_relations_before

        # Create temporal closures for IS_INCLUDED
        closure = Closure(self.text_obj, RelationType.IS_INCLUDED)
        closure_relations_before = closure.get_closure_relations()
        self.text_obj.relations = self.text_obj.relations + closure_relations_before

        # Create temporal closures for DURING
        closure = Closure(self.text_obj, RelationType.DURING)
        closure_relations_before = closure.get_closure_relations()
        self.text_obj.relations = self.text_obj.relations + closure_relations_before

    def _produce_inverse_relations(self):
        relations = self.text_obj.relations
        inversed_relations = []

        for relation in relations:
            # Switching source and target and using inverse of relation
            if relation.relation_type == RelationType.AFTER:
                # Switching AFTER to BEFORE
                inverse_rel = Relation(relation.lid, self.text_obj, relation.source, relation.target, RelationType.BEFORE)
            elif relation.relation_type == RelationType.BEFORE:
                # Switching BEFORE to AFTER
                inverse_rel = Relation(relation.lid, self.text_obj, relation.source, relation.target, RelationType.AFTER)
            elif relation.relation_type == RelationType.INCLUDES:
                # Switching INCLUDES to IS_INCLUDED
                inverse_rel = Relation(relation.lid, self.text_obj, relation.source, relation.target, RelationType.IS_INCLUDED)
            elif relation.relation_type == RelationType.IS_INCLUDED:
                # Switching IS_INCLUDED to INCLUDES
                inverse_rel = Relation(relation.lid, self.text_obj, relation.source, relation.target, RelationType.INCLUDES)
            elif relation.relation_type == RelationType.ENDS:
                # Switching ENDS to ENDED_BY
                inverse_rel = Relation(relation.lid, self.text_obj, relation.source, relation.target, RelationType.ENDED_BY)
            elif relation.relation_type == RelationType.ENDED_BY:
                # Switching ENDED_BY to ENDS
                inverse_rel = Relation(relation.lid, self.text_obj, relation.source, relation.target, RelationType.ENDS)
            elif relation.relation_type == RelationType.DURING:
                # Switching DURING to DURING_INV
                inverse_rel = Relation(relation.lid, self.text_obj, relation.source, relation.target, RelationType.DURING_INV)
            elif relation.relation_type == RelationType.DURING_INV:
                # Switching DURING_INV to DURING
                inverse_rel = Relation(relation.lid, self.text_obj, relation.source, relation.target, RelationType.DURING)
            elif relation.relation_type == RelationType.IAFTER:
                # Switching IAFTER to IBEFORE
                inverse_rel = Relation(relation.lid, self.text_obj, relation.source, relation.target, RelationType.IBEFORE)
            elif relation.relation_type == RelationType.IBEFORE:
                # Switching IBEFORE to IAFTER
                inverse_rel = Relation(relation.lid, self.text_obj, relation.source, relation.target, RelationType.IAFTER)
            else:
                continue

            # Adding relation
            inversed_relations.append(inverse_rel)

        self.text_obj.relations = self.text_obj.relations + inversed_relations

    def _produce_none_relations(self):
        """Produce a NONE-relation between all pairs of events which don't share a relation."""
        print "Producing NONE-relations"
        relations = self.text_obj.relations
        events = self.text_obj.events
        none_relations = []

        for source in events:
            for target in events:
                new_relation = Relation("NONE", self.text_obj, source, target, RelationType.NONE)
                print new_relation

                if new_relation in relations:
                    continue
                else:
                    none_relations.append(new_relation)

        self.text_obj.relations = self.text_obj.relations + none_relations

        print "Finished producing NONE-relations"


    def _produce_all_relations(self):
        """Producing all possible relations."""
        print "Start creating all relations"
        events = self.text_obj.events
        relations = self.text_obj.relations
        all_relations = []

        for source in events:
            for target in events:
                for time in RelationType():
                    new_relation = Relation("all", self.text_obj, source, target, time)

                    if new_relation in relations:
                        continue
                    else:
                        all_relations.append(new_relation)

        print "End creating all relations"
        return all_relations

    def produce_relations(self):
        self._produce_inverse_relations()
        #self._produce_closure_relations()

        # TODO: Trying out if adding NONE relations between pairs of events with no relationship helps the classifier or not
        #self._produce_none_relations()
        self._produce_all_relations()

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

        # Create Timex objects and link them to the Text object
        self._create_timex_objects(text_node, root_node)

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
        for instance in root_node.iterdescendants("MAKEINSTANCE"):
            instance_eid = instance.get("eventID")
            eiid = instance.get("eiid")
            tense = instance.get("tense")
            aspect = instance.get("aspect")
            polarity = instance.get("polarity")
            pos = instance.get("pos")
            modality = instance.get("modality")


            # Get text, sentence, position in sentence and class for event
            text = None
            sentence = None
            e_class = None
            pos_in_sentence = None
            for event in text_node.iterdescendants("EVENT"):
                eid = event.get("eid")
                if instance_eid == eid:
                    text = event.text

                    # Getting surrounding sentence
                    s = Sentence(event)
                    sentence = s.text
                    pos_in_sentence = s.get_position(event)

                    e_class = event.get("class")
                    break

            # Create Event object or append new eiid and append it to Text object
            event_obj = self.text_obj.find_event_by_eid(eid)
            if event_obj:
                # There is already an Event object with this eid but a different eiid
                event_obj.eiid.append(eiid)
            else:
                # There is no Event object yet with this eid
                event_obj = Event(eid, eiid, self.text_obj, text, sentence, pos_in_sentence, e_class, tense, aspect, polarity, pos, modality)
                self.text_obj.append_event(event_obj)

    def _create_timex_objects(self, text_node, root_node):
        for timex in text_node.iterdescendants("TIMEX3"):
            self._create_timex_object(timex)

        # Also looking for timex in <DCT></DCT>
        dct_node = root_node.find("DCT")
        for timex in dct_node.iterdescendants("TIMEX3"):
            self._create_timex_object(timex, dct=True)

    def _create_timex_object(self, timex_node, dct=False):
        # TODO: I should put this directly into parsexml/timex.py
        tid = timex_node.get("tid")
        type = timex_node.get("type")
        value = timex_node.get("value")
        s = Sentence(timex_node)
        sentence = s.text
        pos_in_sentence = s.get_position(timex_node)

        # Create Timex object and append it to Text object
        if dct:
            timex_obj = Timex(tid, type, value, sentence, pos_in_sentence, True)
        else:
            timex_obj = Timex(tid, type, value, sentence, pos_in_sentence, False)

        self.text_obj.append_timex(timex_obj)

    def _create_relation_objects(self, root_node):
        """Must be called after _create_event_objects."""
        for relation in root_node.iterdescendants("TLINK"):
            # Only consider event-event and event-timex relations; Ignoring timex-timex
            if not relation.get("eventInstanceID"):
                continue

            lid = relation.get("lid")
            source_eiid = relation.get("eventInstanceID")

            event_event = True
            if relation.get("relatedToEventInstance"):
                # Event-event relation
                target_eiid = relation.get("relatedToEventInstance")
            else:
                # Event-timex relation
                target_tid = relation.get("relatedToTime")
                event_event = False


            # Get relation type as a string
            relation_type = relation.get("relType")

            # Get relation_type_id
            relation_type_id = RelationType.get_id(relation_type)

            # Find source event
            source_event_obj = self.text_obj.find_event_by_eiid(source_eiid)

            # Find target event or target timex
            if event_event:
                # Event-event
                target_event_obj = self.text_obj.find_event_by_eiid(target_eiid)
                relation_obj = Relation(lid, self.text_obj, source_event_obj, target_event_obj, relation_type_id)
            else:
                # Event-timex
                target_timex_obj = self.text_obj.find_timex_by_tid(target_tid)
                relation_obj = Relation(lid, self.text_obj, source_event_obj, target_timex_obj, relation_type_id)

            self.text_obj.append_relation(relation_obj)


if __name__ == "__main__":
    a = Parser("data/training/TE3-Silver-data/AFP_ENG_19970401.0006.tml")
    a.produce_inverse_relations()
    a.produce_closure_relations()
