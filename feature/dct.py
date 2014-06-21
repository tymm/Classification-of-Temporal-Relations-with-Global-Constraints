from parsexml.timex import Timex

class Dct:
    def __init__(self, relation):
        self._text_obj = relation.parent
        self._a = relation.source
        self._b = relation.target

    def has_dct(self):
        if type(self._a) == Timex:
            if self._a.dct:
                return True

        if type(self._b) == Timex:
            if self._b.dct:
                return True

        return False
