class Event(object):
    def __init__(self, eid, eiid, text_obj, text, e_class, tense, aspect, polarity, pos, modality):
        self.eid = eid
        self.eiid = eiid
        self.parent_node = text_obj
        self.text = text

        # As definied in xml data
        self.e_class = e_class
        self.tense = tense
        self.aspect = aspect
        self.polarity = polarity
        self.pos = pos
        self.modality = modality
