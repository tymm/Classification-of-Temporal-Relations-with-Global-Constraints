from gurobipy import *
from ilp.variable import Variable
from parsexml.relationtype import RelationType

class Constraints:
    def __init__(self, text_obj, test=False):
        self.text_obj = text_obj
        if not test:
            self.directed_pairs = text_obj.directed_pairs
        self.variables = []
        self.model = Model("ILP")
        self.model.setParam(GRB.Param.OutputFlag,0)

        # Run model for text_obj
        if not test:
            self._build_model()

    def _build_model(self):
        try:
            objective_func = LinExpr()

            # Create variables
            for i, pair in enumerate(self.directed_pairs):
                for rel_type in pair.confidence_scores:
                    x = self.model.addVar(vtype=GRB.BINARY, name="x_"+pair.source.id + pair.target.id + str(rel_type))
                    v = Variable(x, pair, rel_type)
                    self.variables.append(v)
                    objective_func += v.confidence_score * x

            self.model.update()

            # Set objective function
            self.model.setObjective(objective_func, GRB.MAXIMIZE)

            # Add constraint i) which says that among all pairs (variables) which represent _one_ relation, there can only be one pair which is set (1).
            constraint_i = {}

            for pair in self.directed_pairs:
                for rel_type in pair.confidence_scores:
                    if constraint_i.has_key(pair):
                        constraint_i[pair] += self._get_variable_by_pair_and_rel_type(pair, rel_type)
                    else:
                        constraint_i[pair] = self._get_variable_by_pair_and_rel_type(pair, rel_type)

                # Add constraint
                self.model.addConstr(constraint_i[pair], GRB.EQUAL, 1, "i")

            # Add constraint ii) which says that all triples of variables which make up a transitive graph should be activated
            constraint_ii = {}

            for triple in self._get_all_transitive_variable_triples():
                i = triple[0].variable
                j = triple[1].variable
                k = triple[2].variable

                self.model.addConstr(i+j-k, GRB.LESS_EQUAL, 1, "ii")

            self.model.optimize()

        except GurobiError:
            print "Gurobi Error reported"

    def _get_all_transitive_variable_triples(self):
        triples = []

        # A before B && B before C => A before C
        rule = ["A", RelationType.BEFORE, "B", "B", RelationType.BEFORE, "C", "A", RelationType.BEFORE, "C"]
        triples += self._get_triples_by_rule(rule)

        # A before B && B includes C => A before C
        rule = ["A", RelationType.BEFORE, "B", "B", RelationType.INCLUDES, "C", "A", RelationType.BEFORE, "C"]
        triples += self._get_triples_by_rule(rule)

        # A before B && B simultaneous C => A before C
        rule = ["A", RelationType.BEFORE, "B", "B", RelationType.SIMULTANEOUS, "C", "A", RelationType.BEFORE, "C"]
        triples += self._get_triples_by_rule(rule)

        # A includes B && B includes C => A includes C
        rule = ["A", RelationType.INCLUDES, "B", "B", RelationType.INCLUDES, "C", "A", RelationType.INCLUDES, "C"]
        triples += self._get_triples_by_rule(rule)

        # A includes B && B simultaneous C => A includes C
        rule = ["A", RelationType.INCLUDES, "B", "B", RelationType.SIMULTANEOUS, "C", "A", RelationType.INCLUDES, "C"]
        triples += self._get_triples_by_rule(rule)

        # A simultaneous B && B before C => A before C
        rule = ["A", RelationType.SIMULTANEOUS, "B", "B", RelationType.BEFORE, "C", "A", RelationType.BEFORE, "C"]
        triples += self._get_triples_by_rule(rule)

        # A simultaneous B && B includes C => A includes C
        rule = ["A", RelationType.SIMULTANEOUS, "B", "B", RelationType.INCLUDES, "C", "A", RelationType.INCLUDES, "C"]
        triples += self._get_triples_by_rule(rule)

        # A simultaneous B && B simultaneous C => A simultaneous C
        rule = ["A", RelationType.SIMULTANEOUS, "B", "B", RelationType.SIMULTANEOUS, "C", "A", RelationType.SIMULTANEOUS, "C"]
        triples += self._get_triples_by_rule(rule)

        # Deduced
        # A simultaneous B && A before C => B before C
        rule = ["A", RelationType.SIMULTANEOUS, "B", "A", RelationType.BEFORE, "C", "B", RelationType.BEFORE, "C"]
        triples += self._get_triples_by_rule(rule)

        # A simultaneous B && A includes C => B includes C
        rule = ["A", RelationType.SIMULTANEOUS, "B", "A", RelationType.INCLUDES, "C", "B", RelationType.INCLUDES, "C"]
        triples += self._get_triples_by_rule(rule)

        return triples

    def _get_triples_by_rule(self, rule):
        # rule = [r1.source, r1.rel_type, r1.target, r2.source, r2.rel_type, r2.target, r3.source, r3.rel_type, r3.target]
        r1_source = rule[0]
        r1_rel_type = rule[1]
        r1_target = rule[2]
        r2_source = rule[3]
        r2_rel_type = rule[4]
        r2_target = rule[5]
        # =>
        r3_source = rule[6]
        r3_rel_type = rule[7]
        r3_target = rule[8]

        if r1_source == r2_source:
            return self._get_triples_source_equal(rule)
        elif r1_source == r2_target:
            return self._get_triples_r1_source_r2_target_equal(rule)
        elif r1_target == r2_target:
            return self._get_triples_target_equal(rule)
        elif r1_target == r2_source:
            return self._get_triples_r1_target_r2_source_equal(rule)

    def _get_triples_r1_target_r2_source_equal(self, rule):
        r1_source= rule[0]
        r1_rel_type = rule[1]

        r2_target = rule[5]
        r2_rel_type = rule[4]

        r3_source = rule[6]
        r3_rel_type = rule[7]
        r3_target = rule[8]

        triples = []

        # Search for variables where r1.target == r2.source
        for v1 in self.variables:
            for v2 in self.variables:
                if v1.target == v2.source:
                    if v1.relation_type == r1_rel_type and v2.relation_type == r2_rel_type:
                        transitive = self._find_transitive(v1.source, v2.target, rule)
                        if transitive:
                            triples.append([v1, v2, transitive])

        return triples

    def _get_triples_r1_source_r2_target_equal(self, rule):
        r1_source= rule[0]
        r1_rel_type = rule[1]

        r2_target = rule[5]
        r2_rel_type = rule[4]

        r3_source = rule[6]
        r3_rel_type = rule[7]
        r3_target = rule[8]

        triples = []

        # Search for variables where r1.target == r2.source
        for v1 in self.variables:
            for v2 in self.variables:
                if v1.source == v2.target:
                    if v1.relation_type == r1_rel_type and v2.relation_type == r2_rel_type:
                        transitive = self._find_transitive(v1.target, v2.source, rule)
                        if transitive:
                            triples.append([v1, v2, transitive])

        return triples

    def _get_triples_target_equal(self, rule):
        r1_source= rule[0]
        r1_rel_type = rule[1]

        r2_target = rule[5]
        r2_rel_type = rule[4]

        r3_source = rule[6]
        r3_rel_type = rule[7]
        r3_target = rule[8]

        triples = []

        # Search for variables where r1.target == r2.target
        for v1 in self.variables:
            for v2 in self.variables:
                if v1.target == v2.target:
                    if v1.relation_type == r1_rel_type and v2.relation_type == r2_rel_type:
                        transitive = self._find_transitive(v1.source, v2.source, rule)
                        if transitive:
                            triples.append([v1, v2, transitive])

        return triples

    def _get_triples_source_equal(self, rule):
        r1_target = rule[2]
        r1_rel_type = rule[1]
        r2_target = rule[5]
        r2_rel_type = rule[4]

        r3_source = rule[6]
        r3_rel_type = rule[7]
        r3_target = rule[8]

        triples = []

        # Search for variables with same source
        for v1 in self.variables:
            for v2 in self.variables:
                if v1.source == v2.source:
                    if v1.relation_type == r1_rel_type and v2.relation_type == r2_rel_type:
                        transitive = self._find_transitive(v1.target, v2.target, rule)
                        if transitive:
                            triples.append([v1, v2, transitive])

        return triples

    def _find_transitive(self, source, target, rule):
        r3_rel_type = rule[7]

        for variable in self.variables:
            if variable.source == source and variable.target == target and variable.relation_type == r3_rel_type:
                return variable
        else:
            return None

    def _get_variable_by_pair_and_rel_type(self, pair, rel_type):
        for variable in self.variables:
            if variable.pair == pair and variable.relation_type == rel_type:
                return variable.variable
        else:
            return None

    def get_best_set(self):
        best_subset = []

        for v in self.variables:
            # Check if variable has value 1.0 which means it is set
            if v.variable.getAttr("x") == 1.0:
                relation = self.text_obj.find_relation_by_variable(v)
                # Relation does not have to exist
                if relation:
                    best_subset.append(relation)
                else:
                    # The relation exists but with a different relation type
                    rel_type = v.relation_type

                    # Find relation with source and target
                    relation = self.text_obj.find_relation_by_source_and_target(v.source, v.target)
                    # Change relation type
                    relation.relation_type = rel_type

                    best_subset.append(relation)

        return best_subset
