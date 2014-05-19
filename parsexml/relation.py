from parsexml.timex import Timex

class Relation:
    def __init__(self, lid, text_obj, source_obj, target_obj, relation_type_id):
        self.lid = lid
        self.parent = text_obj
        self.source = source_obj
        self.target = target_obj
        self.relation_type = relation_type_id
        self.is_timex = None

        self._check_timex()

    def is_event_timex(self):
        if self.is_timex:
            return True
        else:
            return False

    def is_event_event(self):
        return not self.is_event_timex()

    def _check_timex(self):
        """Check if this relation is an event-event relation or an event-timex relation."""
        if type(self.source) is Timex or type(self.target) is Timex:
            self.is_timex = True
        else:
            self.is_timex = False

