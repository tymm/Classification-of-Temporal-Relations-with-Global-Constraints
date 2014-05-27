from lxml import etree

class Text:
    def __init__(self, file):
        self.file = file
        self.text = None
        self.events = []
        self.timex = []
        self.relations = []
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

    def build_entity_order(self):
        tree = etree.parse(self.file)
        root_node = tree.getroot()

        text_node = root_node.find("TEXT")

        for entity_node in text_node:
            eid = entity_node.get("eid")
            if eid:
                # It's an event
                entity = self.find_event_by_eid(eid)
            else:
                # It's a timex
                tid = entity_node.get("tid")
                entity = self.find_timex_by_tid(tid)

            self.entities_order.append(entity)
