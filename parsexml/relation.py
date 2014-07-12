from parsexml.timex import Timex

class Relation:
    def __init__(self, lid, text_obj, source_obj, target_obj, relation_type_id):
        self.lid = lid
        self.parent = text_obj
        self.filename = self.parent.filename
        self.source = source_obj
        self.target = target_obj
        self.relation_type = relation_type_id
        self._is_timex = None

        self._check_timex()

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash(self.filename + str(self.source.__hash__()) + str(self.target.__hash__()))

    def get_result(self):
        return self.relation_type

    def is_event_timex(self):
        if self._is_timex:
            return True
        else:
            return False

    def is_event_event(self):
        return not self.is_event_timex()

    def _check_timex(self):
        """Check if this relation is an event-event relation or an event-timex relation."""
        if type(self.source) is Timex or type(self.target) is Timex:
            self._is_timex = True
        else:
            self._is_timex = False

