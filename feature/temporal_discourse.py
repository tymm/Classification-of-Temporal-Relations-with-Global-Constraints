import re

class Temporal_discourse:
    def __init__(self, relation, discourse_cache, nlp_persistence_obj):
        # This feature works only for entities which are in the same sentence
        if not relation.source.sentence == relation.target.sentence:
            raise EntitiesNotInSameSentence

        self.relation = relation
        self.source = relation.source
        self.target = relation.target
        self.sentence = self.target.sentence
        self.text_structure = relation.parent.text_structure

        self.nlp_persistence_obj = nlp_persistence_obj
        self.discourse_cache = discourse_cache.data

        self.parsetree = self._get_discourse_parsetree()
        self.connective_tag = self._identify_connective_tag()
        self.begin_connective_tag, self.end_connective_tag = self._get_position()

    def _get_discourse_parsetree(self):
        discourse_parsetree = self.discourse_cache[self.sentence]
        return discourse_parsetree

    def _identify_connective_tag(self):
        # Expansion, Contingency, Comparison, Temporal, or 0
        # Output could look like this:
        # (ROOT (S (NP (NNP John)) (VP (VBZ has) (VP (VBN been) (VP (VBG taking) (NP (NP (DT that) (VBG driving) (NN course)) (SBAR (IN since#0#Contingency) (S (NP (PRP he)) (VP (VBZ wants) (S (VP (TO to) (VP (VB drive) (NP (JJR better)))))))))))) (. .)))

        match = re.search(r" (.*)#\d#(Temporal|Expansion|Comparison|Contingency|0)", self.parsetree)

        if match:
            return match.group(1)
        else:
            raise NoConnectiveTagFound

    def _get_position(self):
        if self.connective_tag:
            sentence_text = self.sentence.text

            begin = sentence_text.find(self.connective_tag)
            end = begin + len(self.connective_tag)

            return (begin, end)
        else:
            raise NoConnectiveTagFound

    def is_temporal(self):
        if "#Temporal" in self.parsetree:
            return True
        else:
            return False

    def is_connective_tag_at_beginning(self):
        if self.begin_connective_tag == 0:
            return True
        else:
            return False

    def entity_before_connective_tag(self, event):
        if event.begin < self.begin_connective_tag:
            return True
        else:
            return False

class EntitiesNotInSameSentence(Exception):
    def __str__(self):
        return repr("Temporal discourse feature only works for entities with the same sentence.")

class NoConnectiveTagFound(Exception):
    def __str__(self):
        return repr("Temporal discourse feature only works for entities with the same sentence.")
