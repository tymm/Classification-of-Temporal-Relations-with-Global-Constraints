from lxml import etree
from parsexml.sentence import Sentence
from parsexml.parser import Parser

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
