class Same_class:
    def __init__(self, relation):
        self.relation = relation

    def is_same(self):
        if self.relation.source.e_class == self.relation.target.e_class:
            return True
        else:
            return False
