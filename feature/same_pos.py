class Same_pos:
    def __init__(self, relation):
        self.relation = relation

    def is_same(self):
        if self.relation.source.pos == self.relation.target.pos:
            return True
        else:
            return False
