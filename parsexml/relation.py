from parsexml.timex import Timex
from parsexml.event import Event

class Relation(object):
    def __init__(self, lid, text_obj, source_obj, target_obj, relation_type_id):
        self.lid = lid
        self.parent = text_obj
        self.filename = self.parent.filename
        self.source = source_obj
        self.target = target_obj
        self.relation_type = relation_type_id

        self._is_event_timex = False
        self._is_event_event = False
        self._is_timex_timex = False

        self.feature = None
        self.confidence_score = None
        self.predicted_class = None

        self._check_if_event_event_or_event_timex()

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash(self.filename + str(self.source.__hash__()) + str(self.target.__hash__()) + str(self.relation_type))

    def get_result(self):
        return self.relation_type

    def get_feature(self):
        return self.feature

    def set_feature(self, feature):
        self.feature = feature

    def is_event_timex(self):
        if self._is_event_timex:
            return True
        else:
            return False

    def is_event_event(self):
        if self._is_event_event:
            return True
        else:
            return False

    def is_timex_timex(self):
        if self._is_timex_timex:
            return True
        else:
            return False

    def _check_if_event_event_or_event_timex(self):
        """Check if this relation is an event-event relation or an event-timex relation."""
        if (type(self.source) is Timex and type(self.target) is Event) or (type(self.source) is Event and type(self.target) is Timex):
            self._is_event_timex = True
        elif type(self.source) is Event and type(self.target) is Event:
            self._is_event_event = True
        elif type(self.source) is Timex and type(self.target) is Timex:
            self._is_timex_timex = True
