from parsexml.timex import Timex

class Dct:
    def __init__(self, relation):
        self.source = relation.source
        self.target = relation.target

    def has_dct(self):
        if type(self.source) == Timex:
            if self.source.is_dct:
                return True

        if type(self.target) == Timex:
            if self.target.is_dct:
                return True

        return False
