from parsexml.event import Event

class Token:
    def __init__(self, relation, strings_cache):
        self.relation = relation
        self.cache = strings_cache.tokens

        if type(self.relation.source) == Event:
            try:
                self.source = self.cache.index(self.relation.source.text.lower())
            except ValueError:
                # String is not known from training set
                self.source = len(self.cache)
        else:
            self.source = len(self.cache) + 1

        if type(self.relation.target) == Event:
            try:
                self.target = self.cache.index(self.relation.target.text.lower())
            except ValueError:
                # String is not known from training set
                self.target = len(self.cache)
        else:
            self.target = len(self.cache) + 1

    def get_length(self):
        return len(self.cache) + 2
