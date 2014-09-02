from parsexml.event import Event

class Tense(object):
    PRESENT = 0
    PAST = 1
    FUTURE = 2
    INFINITIVE = 3
    PRESPART = 4
    PASTPART = 5
    NONE = 6

    def __init__(self, relation):
        self.relation = relation
        self.source = self._get_source()
        self.target = self._get_target()

    @classmethod
    def get_length(cls):
        return 7

    def _get_source(self):
        source = self.relation.source

        if type(source) == Event:
            return self._determine_tense(source.tense)
        else:
            return Tense.NONE

    def _get_target(self):
        target = self.relation.target

        if type(target) == Event:
            return self._determine_tense(target.tense)
        else:
            return Tense.NONE

    def _determine_tense(self, text):
        if text == "PRESENT":
            return Tense.PRESENT
        elif text == "PAST":
            return Tense.PAST
        elif text == "FUTURE":
            return Tense.FUTURE
        elif text == "INFINITIVE":
            return Tense.INFINITIVE
        elif text == "PRESPART":
            return Tense.PRESPART
        elif text == "PASTPART":
            return Tense.PASTPART
        else:
            return Tense.NONE
