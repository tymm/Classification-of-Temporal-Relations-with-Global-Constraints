class Same_aspect:
    def __init__(self, relation):
        self.relation = relation

    def is_same(self):
        if self.relation.source.aspect == self.relation.target.aspect:
            return True
        else:
            return False
