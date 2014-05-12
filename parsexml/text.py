class Text:
    def __init__(self, file, text):
        self.file = file
        self.text = text
        self.events = []

    def append_event(self, event):
        self.events.append(event)
