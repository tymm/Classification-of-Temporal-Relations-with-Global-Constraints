from lxml import etree
from parsexml.sentence import Sentence
from parsexml.text_structure import Text_structure

class Text:
    def __init__(self, filename):
        self.filename = filename
        self.text = None
        self.events = []
        self.timex = []
        self.relations = []
        self.text_structure = None
        self.entities_order = []

    def set_text(self, text):
        self.text = text

    def append_event(self, event):
        self.events.append(event)

    def append_timex(self, timex):
        self.timex.append(timex)

    def append_relation(self, relation):
        self.relations.append(relation)

    def find_event_by_eiid(self, eiid):
        for event in self.events:
            if event.eiid == eiid:
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

    def build_text_structure(self):
        """Must be called after all entities got appended."""
        structure = Text_structure(self)
        self.entities_order = structure.get_entities_ordered()
        self.text_structure = structure
