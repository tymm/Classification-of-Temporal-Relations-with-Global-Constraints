from feature.dependency import Dependency
from nltk import word_tokenize

class Dependency_order(Dependency):
    def __init__(self, relation, nlp_persistence_obj):
        Dependency.__init__(self, relation, nlp_persistence_obj)

    def get_dependency_order(self):
        if self.relation.source == self.relation.target:
            return 2

        if self._check_if_relation_is_in_same_sentence():
            # Who is governing who
            if self._is_e1_governing_e2(self.source, self.target):
                return 0
            else:
                return 1
        else:
            return None

    def _is_e1_governing_e2(self, e1_text, e2_text):
        children = self._find_children(e1_text)

        if e2_text in children:
            return True
        else:
            if len(children) == 0:
                return False
            else:
                r = []
                for child in children:
                    r.append(self._is_e1_governing_e2(child, e2_text))

                if True in r:
                    return True
                else:
                    return False

    def _find_children(self, entity):
        children = []

        for dependency in self.collapsed_dependencies:
            if dependency[1] == entity:
                children.append(dependency[2])

        return children
