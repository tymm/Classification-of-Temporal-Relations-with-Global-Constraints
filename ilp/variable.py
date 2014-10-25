class Variable(object):
    def __init__(self, variable, pair, relation_type):
        self.variable = variable
        self.pair = pair
        self.source = self.pair.source
        self.target = self.pair.target
        self.relation_type = relation_type
        self.confidence_score = self.pair.confidence_scores[self.relation_type]
