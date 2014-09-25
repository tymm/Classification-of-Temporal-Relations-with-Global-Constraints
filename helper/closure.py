from parsexml.relation import Relation
from parsexml.relationtype import RelationType

class Closure:
    def __init__(self, text_obj, relation_type):
        self.text_obj = text_obj
        self.relation_type = relation_type
        # Copy. Don't reference
        self.relations = list(self.text_obj.relations)
        self.new_relations = self._generate_closure_relations()

    def get_closure_relations(self):
        return self.new_relations

    def _generate_closure_relations(self):
        closures = []

        new_closures = self._generate_closures()
        closures += new_closures

        while len(new_closures) != 0:
            new_closures = self._generate_closures()
            closures += new_closures

        return closures

    def _generate_closures(self):
        relations = [r for r in self.relations if r.relation_type == self.relation_type]
        closures = []

        for relation in relations:
            source = relation.source
            target = relation.target

            for rel in relations:
                if target == rel.source:
                    closure = self._create_closured_relation(source, rel.target)
                    if closure not in self.relations and closure not in closures:
                        closures.append(closure)

        self.relations += closures
        return closures

    def _create_closured_relation(self, source, target):
        rel = Relation("closure", self.text_obj, source, target, self.relation_type)
        return rel
