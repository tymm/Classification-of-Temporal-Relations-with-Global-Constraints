class Text:
    def __init__(self, file):
        self.file = file
        self.text = None
        self.events = []
        self.relations = []

    def set_text(self, text):
        self.text = text

    def append_event(self, event):
        self.events.append(event)

    def append_relation(self, relation):
        self.relations.append(relation)

    def find_event_by_eid(self, eid):
        for event in self.events:
            if event.eid == eid:
                return event

        return None
