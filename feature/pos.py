from parsexml.event import Event

class Pos:
    def __init__(self, relation, nlp_persistence_obj):
        self.relation = relation
        self.nlp_persistence_obj = nlp_persistence_obj

        self.tags = ['PRP$', 'VBG', 'VBD', 'VBN', 'VBP', 'JJ', 'VBZ', 'DT', 'RP', 'NN', 'FW', 'POS', 'TO', 'LS', 'RB', ':', 'NNS', 'PRP', 'VB', 'WRB', 'CC', 'PDT', 'CD', 'IN', 'MD', 'NNPS', 'JJS', 'JJR', 'SYM', 'UH', 'NNP', '$']

        self.source = self._get_pos_tag(self.relation.source)
        self.target = self._get_pos_tag(self.relation.target)

    def get_length(self):
        return len(self.tags) + 1

    def _get_pos_tag(self, entity):
        if type(entity) == Event:
            sentence = entity.sentence
            word = entity.text
            pos_tag = self.nlp_persistence_obj.get_pos_tag_for_word(sentence, word)

            return self.tags.index(pos_tag)
        else:
            return len(self.tags)
