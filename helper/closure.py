from parsexml.relation import Relation
from parsexml.relationtype import RelationType
import numpy as np

class Closure:
    def __init__(self, text_obj, relation_type, transitives_of_transitives=False):
        """If transitives_of_transitives is True we will calculate all possible transitives. Otherwise it will only be returned direct transitives."""
        self.transitives_of_transitives = transitives_of_transitives
        self.text_obj = text_obj
        self.relations = text_obj.relations
        self.relation_type = relation_type

    def get_closure_relations(self):
        if self.transitives_of_transitives:
            closures = self._generate_all_closures(self.relations)
            return closures

        else:
            closures = self._generate_closure_relations(self.relations)
            return closures

    def _generate_all_closures(self, relations):
        all_closures = []

        new_closures = self._generate_closure_relations(relations)
        all_closures += new_closures

        while len(new_closures) != 0:
            closures = set(self._generate_closure_relations(relations + all_closures))
            new_closures = closures.difference(set(relations+all_closures))
            all_closures += new_closures

        return all_closures

    def _generate_closure_relations(self, relations):
        relevant_relations = self._get_relevant_relations(relations)

        matrix = self._generate_boolean_matrix_from_relations(relevant_relations)
        matrix_with_transitives_as_ones = matrix.dot(matrix)

        closured = self._build_closured_relations_from_matrix(matrix_with_transitives_as_ones, relevant_relations)

        return closured

    def _get_relevant_relations(self, relations):
        relevant_relations = [r for r in relations if r.relation_type == self.relation_type]

        return relevant_relations

    def _build_closured_relations_from_matrix(self, matrix, relevant_relations):
        closured = []

        entities = self._generate_entities_list(relevant_relations)
        n = len(entities)

        for source in range(n):
            for target in range(n):
                if matrix[source][target] >= 1:
                    source_enitity = entities[source]
                    target_entity = entities[target]
                    closured.append(self._create_closured_relation(source_enitity, target_entity))

        return closured

    def _generate_entities_list(self, relevant_relations):
        entities = []

        for relation in relevant_relations:
            e1 = relation.source
            e2 = relation.target

            if e1 not in entities:
                entities.append(e1)
            if e2 not in entities:
                entities.append(e2)

        return entities

    def _generate_boolean_matrix_from_relations(self, relevant_relations):
        entities = self._generate_entities_list(relevant_relations)

        n = len(entities)
        matrix = np.zeros([n,n])

        for relation in relevant_relations:
            index_entities_source = entities.index(relation.source)
            index_entities_target = entities.index(relation.target)

            matrix[index_entities_source][index_entities_target] = 1

        return matrix

    def _create_closured_relation(self, source, target):
        rel = Relation("closure", self.text_obj, source, target, self.relation_type)
        return rel
