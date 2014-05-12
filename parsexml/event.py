class Event:
    def __init__(self, eid, text_obj, text):
        self.eid = eid
        self.parent_node = text_obj
        self.text = text
