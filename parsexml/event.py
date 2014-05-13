class Event:
    def __init__(self, eid, eiid, text_obj, text):
        self.eid = eid
        self.eiid = eiid
        self.parent_node = text_obj
        self.text = text
