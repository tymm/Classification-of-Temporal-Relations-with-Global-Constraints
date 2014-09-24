from feature.dependency import Dependency

class Dependency_root(Dependency):
    def __init__(self, relation, nlp_persistence_obj):
        Dependency.__init__(self, relation, nlp_persistence_obj)
        self.value_source = None
        self.value_target = None

    def get_dependency_is_root(self):
        if self._check_if_relation_is_in_same_sentence():
            # Describes whether either the source or target entity is root or not
            is_source_root = self.nlp_persistence_obj.is_root(self.relation.source)
            is_target_root = self.nlp_persistence_obj.is_root(self.relation.target)

            if is_source_root == True:
                self.value_source = 1
            else:
                self.value_source = 0

            if is_target_root == True:
                self.value_target = 1
            else:
                self.value_target = 0
