class Polarity:
    def __init__(self, relation):
        self.relation = relation

        if self._is_source_pos():
            self.source = 1
        else:
            self.source = 0

        if self._is_target_pos():
            self.target = 1
        else:
            self.target = 0

    def _is_source_pos(self):
        if self.relation.source.pos == "POS":
            return True
        else:
            return False

    def _is_target_pos(self):
        if self.relation.target.pos == "POS":
            return True
        else:
            return False
