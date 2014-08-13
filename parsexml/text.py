from lxml import etree
from parsexml.sentence import Sentence
from parsexml.parser import Parser
from parsexml.relationtype import RelationType
from parsexml.relation import Relation
from Feature import Feature

class Text:
    def __init__(self, filename):
        self.filename = filename

        # Parse text
        parser = Parser(filename, self)

        self.text = parser.get_text()
        self.events = parser.get_events()
        self.timex = parser.get_timex()
        self.relations = parser.get_relations()
        self.text_structure = parser.get_text_structure()
        self.entities_order = parser.get_entities_order()

    def find_event_by_eiid(self, eiid):
        for event in self.events:
            if eiid in event.eiid:
                return event

        return None

    def find_event_by_eid(self, eid):
        for event in self.events:
            if event.eid == eid:
                return event

        return None

    def find_timex_by_tid(self, tid):
        for timex in self.timex:
            if timex.tid == tid:
                return timex

        return None

    def create_all_relations_and_features(self):
        """Creating all possible relations between all entities.

        Creating features here for performance.
        """
        all_relations = []

        feature = None

        for source in self.events + self.timex:
            for target in self.events + self.timex:
                for i, time in enumerate(RelationType()):
                    new_relation = Relation("all", self, source, target, time)

                    # We don't have the feature yet
                    if i == 0:
                        f = Feature(new_relation)
                        feature = f.get_feature()

                    if new_relation in self.relations:
                        continue
                    else:
                        new_relation.set_feature(feature)
                        all_relations.append(new_relation)

                feature = None

        self.relations = self.relations + all_relations
