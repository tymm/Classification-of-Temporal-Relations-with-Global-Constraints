class Text:
    def __init__(self, file):
        self.file = file
        self.text = None
        self.events = []
        self.timex = []
        self.relations = []

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

    def find_timex_by_tid(self, tid):
        for timex in self.timex:
            if timex.tid == tid:
                return timex

        return None
