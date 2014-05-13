class Text:
    def __init__(self, file):
        self.file = file
        self.text = text
        self.events = []

    def set_text(self, text):
        self.text = text

    def append_event(self, event):
        self.events.append(event)

    def find_event_by_eid(self, eid):
        for event in self.events:
            if event.eid == eid:
                return event

        return None
