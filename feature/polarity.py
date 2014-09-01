from parsexml.event import Event

class Polarity:
    def __init__(self, relation):
        self.relation = relation

        if not type(self.relation.source) == Event:
            self.source = 2
        elif self.relation.source.pos == "POS":
            self.source = 1
        else:
            self.source = 0

        if not type(self.relation.target) == Event:
            self.target = 2
        elif self.relation.target.pos == "POS":
            self.target = 1
        else:
            self.target = 0
