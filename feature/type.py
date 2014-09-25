from parsexml.timex import Timex

class Type:
    """Timex.type can be 'DATE' | 'TIME' | 'DURATION' | 'SET'."""
    def __init__(self, relation):
        source = relation.source
        target = relation.target

        if type(source) == Timex:
            self.source = self._get_type(source)
        else:
            self.source = 4

        if type(target) == Timex:
            self.target = self._get_type(target)
        else:
            self.target = 4

    def _get_type(self, timex):
        if timex.type == "DATE":
            return 0
        elif timex.type == "TIME":
            return 1
        elif timex.type == "DURATION":
            return 2
        elif timex.type == "SET":
            return 3
