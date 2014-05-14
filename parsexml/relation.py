class Relation:
    def __init__(self, lid, text_obj, source_event_obj, target_obj, relation_type_id, timex=False):
        self.lid = lid
        self.parent = text_obj
        self.source_event = source_event_obj
        self.target = target_obj
        self.relation_type = relation_type_id
        self.timex = timex

    def is_event_timex(self):
        if self.timex:
            return True
        else:
            return False

    def is_event_event(self):
        return not self.is_event_timex()
