class Same_polarity:
    def __init__(self, relation):
        self.relation = relation

    def is_same(self):
        if self.relation.source.polarity == self.relation.target.polarity:
            return True
        else:
            return False
