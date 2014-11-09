from helper.nlp_persistence import LemmaNotFound
class Lemma:
    def __init__(self, relation, strings_cache, nlp_persistence_obj):
        self.relation = relation
        self.cache = strings_cache.lemmas
        self.nlp_persistence_obj = nlp_persistence_obj

        try:
            self.source = self.cache.index(self._get_lemma(self.relation.source).lower())
        except (ValueError, LemmaNotFound):
            # TODO: When LemmaNotFound, get lemma manually
            # String is not known from training set
            self.source = len(self.cache)

        try:
            self.target = self.cache.index(self._get_lemma(self.relation.target).lower())
        except (ValueError, LemmaNotFound):
            # TODO: When LemmaNotFound, get lemma manually
            # String is not known from training set
            self.target = len(self.cache)

    def get_length(self):
        return len(self.cache) + 1

    def _get_lemma(self, entity):
        return self.nlp_persistence_obj.get_lemma_for_word(entity.sentence, entity.text)
