from gurobipy import *

class Constraints:
    def __init__(self, relations):
        self.relations = relations
        self.transitives = self._get_transitive_relations(relations)
        self.variables = []

    def _get_transitive_relations(self, relations):
        # TODO: Only gets one transitive graph when there are more than one
        transitives = []

        for relation in relations:
            continued_relation = self._find_continued_relation(relations, relation)
            if not continued_relation:
                continue

            transitive_relation = self._find_transitive_relation(relations, relation.source, continued_relation.target, relation.relation_type)

            if transitive_relation:
                transitives.append([(relation, continued_relation), transitive_relation])

        return transitives

    def _find_continued_relation(self, relations, relation):
        for r in relations:
            if r.source == relation.target and r.relation_type== relation.relation_type:
                return r
        else:
            return None

    def _find_transitive_relation(self, relations, source, target, relation_type):
        for r in relations:
            if r.source == source and r.target == target and r.relation_type == relation_type:
                return r
        else:
            return None

    def _relations_without_time(self):
        # Get a subset which only includes relations with different source and target entities
        distinct = []

        for relation in self.relations:
            if self._is_not_inside_list_with_same_source_and_target(distinct, relation):
                distinct.append(relation)

        return distinct

    def _is_not_inside_list_with_same_source_and_target(self, distinct_list, relation):
        for r in distinct_list:
            if r.source == relation.source and r.target == relation.target:
                return False

        else:
            return True

    def _find_variable_by_object(self, relation_obj):
        for variable in self.variables:
            if variable[1] == relation_obj:
                return variable[0]
        else:
            return None

    def _build_model(self):
        try:
            m = Model("ILP")
            objective_func = LinExpr()

            # Create variables
            for i, relation in enumerate(self.relations):
                x = m.addVar(vtype=GRB.BINARY, name="x_"+relation.source.name + relation.target.name + str(relation.type))
                self.variables.append((x, relation))
                objective_func += relation.confidence_score * x

            m.update()

            # Set objective function
            m.setObjective(objective_func, GRB.MAXIMIZE)

            # Add constraint i)
            constraint_i = {}

            # relations_without_time() returns a subset which only includes relations with different source and target entities
            for relation in self._relations_without_time():
                source_hash = relation.source.__hash__()
                target_hash = relation.target.__hash__()

                # Get all variables which share the same source and target entity
                variables_rel = self._get_variables_with_same_relation(source_hash, target_hash)

                for variable in variables_rel:
                    if constraint_i.has_key(source_hash+target_hash):
                        constraint_i[source_hash+target_hash] += variable
                    else:
                        constraint_i[source_hash+target_hash] = variable

                # Add constraint
                m.addConstr(constraint_i[source_hash+target_hash], GRB.EQUAL, 1, "i")

            # Add constraint ii)
            constraint_ii = {}

            for transitive in self.transitives:
                a = self._find_variable_by_object(transitive[0][0])
                b = self._find_variable_by_object(transitive[0][1])
                c = self._find_variable_by_object(transitive[1])

                m.addConstr(a+b-c, GRB.LESS_EQUAL, 1, "ii")

            m.optimize()

        except GurobiError:
            print "Gurobi Error reported"

    def return_best_subset(self):
        best_subset = []

        for v in self.variables:
            # Check if variable has value 1.0 which means it is set
            if v[0].getAttr("x") == 1.0:
                relation = v[1]
                best_subset.append(relation)

        return best_subset

