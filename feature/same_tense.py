class Same_tense:
    def __init__(self, relation):
        self.relation = relation

    def is_same(self):
        if self.relation.source.tense == self.relation.target.tense:
            return True
        else:
            return False
