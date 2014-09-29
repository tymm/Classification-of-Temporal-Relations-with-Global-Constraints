class Same_pos:
    def __init__(self, relation, nlp_persistence_obj):
        self.relation = relation
        self.nlp_persistence_obj = nlp_persistence_obj

    def is_same(self):
        if self._get_pos_tag(self.relation.source) == self._get_pos_tag(self.relation.target):
            return True
        else:
            return False

    def _get_pos_tag(self, entity):
        sentence = entity.sentence
        word = entity.text
        pos_tag = self.nlp_persistence_obj.get_pos_tag_for_word(sentence, word)

        return pos_tag
