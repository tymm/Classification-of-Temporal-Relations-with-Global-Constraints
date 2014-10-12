class Strings:
    def __init__(self, relation, strings_cache):
        self.relation = relation
        self.cache = strings_cache

        try:
            self.source = self.cache.index(self.relation.source.text)
        except:
            # String is not known from training set
            self.source = len(self.cache)

        try:
            self.target = self.cache.index(self.relation.target.text)
        except:
            # String is not known from training set
            self.target = len(self.cache)

    def get_length(self):
        return len(self.cache) + 1
