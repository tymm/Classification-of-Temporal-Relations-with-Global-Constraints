from Data import Data
from System import System
from parsexml.relationtype import RelationType

def get_transitives(relations):
    triples = []

    # A before B && B before C => A before C
    rule = ["A", RelationType.BEFORE, "B", "B", RelationType.BEFORE, "C", "A", RelationType.BEFORE, "C"]
    triples += self._get_triples_by_rule(relations, rule)

    # A before B && B includes C => A before C
    rule = ["A", RelationType.BEFORE, "B", "B", RelationType.INCLUDES, "C", "A", RelationType.BEFORE, "C"]
    triples += self._get_triples_by_rule(relations, rule)

    # A before B && B simultaneous C => A before C
    rule = ["A", RelationType.BEFORE, "B", "B", RelationType.SIMULTANEOUS, "C", "A", RelationType.BEFORE, "C"]
    triples += self._get_triples_by_rule(relations, rule)

    # A includes B && B includes C => A includes C
    rule = ["A", RelationType.INCLUDES, "B", "B", RelationType.INCLUDES, "C", "A", RelationType.INCLUDES, "C"]
    triples += self._get_triples_by_rule(relations, rule)

    # A includes B && B simultaneous C => A includes C
    rule = ["A", RelationType.INCLUDES, "B", "B", RelationType.SIMULTANEOUS, "C", "A", RelationType.INCLUDES, "C"]
    triples += self._get_triples_by_rule(relations, rule)

    # A simultaneous B && B before C => A before C
    rule = ["A", RelationType.SIMULTANEOUS, "B", "B", RelationType.BEFORE, "C", "A", RelationType.BEFORE, "C"]
    triples += self._get_triples_by_rule(relations, rule)

    # A simultaneous B && B includes C => A includes C
    rule = ["A", RelationType.SIMULTANEOUS, "B", "B", RelationType.INCLUDES, "C", "A", RelationType.INCLUDES, "C"]
    triples += self._get_triples_by_rule(relations, rule)

    # A simultaneous B && B simultaneous C => A simultaneous C
    rule = ["A", RelationType.SIMULTANEOUS, "B", "B", RelationType.SIMULTANEOUS, "C", "A", RelationType.SIMULTANEOUS, "C"]
    triples += self._get_triples_by_rule(relations, rule)

    # Deduced
    # A simultaneous B && A before C => B before C
    rule = ["A", RelationType.SIMULTANEOUS, "B", "A", RelationType.BEFORE, "C", "B", RelationType.BEFORE, "C"]
    triples += self._get_triples_by_rule(relations, rule)

    # A simultaneous B && A includes C => B includes C
    rule = ["A", RelationType.SIMULTANEOUS, "B", "A", RelationType.INCLUDES, "C", "B", RelationType.INCLUDES, "C"]
    triples += self._get_triples_by_rule(relations, rule)

    # New (inverses)
    # A after B && B after C => A after C
    rule = ["A", RelationType.AFTER, "B", "B", RelationType.AFTER, "C", "A", RelationType.AFTER, "C"]
    triples += self._get_triples_by_rule(relations, rule)

    # A after B && B includes C => A after C
    rule = ["A", RelationType.AFTER, "B", "B", RelationType.INCLUDES, "C", "A", RelationType.AFTER, "C"]
    triples += self._get_triples_by_rule(relations, rule)

    # A after B && B simultaneous C => A after C
    rule = ["A", RelationType.AFTER, "B", "B", RelationType.SIMULTANEOUS, "C", "A", RelationType.AFTER, "C"]
    triples += self._get_triples_by_rule(relations, rule)

    # A is_included B && B is_included C => A is_included C
    rule = ["A", RelationType.IS_INCLUDED, "B", "B", RelationType.IS_INCLUDED, "C", "A", RelationType.IS_INCLUDED, "C"]
    triples += self._get_triples_by_rule(relations, rule)

    # A is_included B && B simultaneous C => A is_included C
    rule = ["A", RelationType.IS_INCLUDED, "B", "B", RelationType.SIMULTANEOUS, "C", "A", RelationType.IS_INCLUDED, "C"]
    triples += self._get_triples_by_rule(relations, rule)

    # A is_included B && B after C => A after C
    rule = ["A", RelationType.IS_INCLUDED, "B", "B", RelationType.AFTER, "C", "A", RelationType.AFTER, "C"]
    triples += self._get_triples_by_rule(relations, rule)

    # A is_included B && B before C => A before C
    rule = ["A", RelationType.IS_INCLUDED, "B", "B", RelationType.BEFORE, "C", "A", RelationType.BEFORE, "C"]
    triples += self._get_triples_by_rule(relations, rule)

    return triples

def _get_triples_by_rule(relations, rule):
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
        return self._get_triples_source_equal(relations, rule)
    elif r1_source == r2_target:
        return self._get_triples_r1_source_r2_target_equal(relations, rule)
    elif r1_target == r2_target:
        return self._get_triples_target_equal(relations, rule)
    elif r1_target == r2_source:
        return self._get_triples_r1_target_r2_source_equal(relations, rule)

def _get_triples_r1_target_r2_source_equal(relations, rule):
    r1_source= rule[0]
    r1_rel_type = rule[1]

    r2_target = rule[5]
    r2_rel_type = rule[4]

    r3_source = rule[6]
    r3_rel_type = rule[7]
    r3_target = rule[8]

    triples = []

    # Search for variables where r1.target == r2.source
    for r1 in relations:
        for r2 in relations:
            if r1.target == r2.source:
                if r1.relation_type == r1_rel_type and r2.relation_type == r2_rel_type:
                    transitive = _find_transitive(relations, r1.source, r2.target, rule)
                    if transitive:
                        triples.append([r1, r2, transitive])

    return triples

def _get_triples_r1_source_r2_target_equal(relations, rule):
    r1_source= rule[0]
    r1_rel_type = rule[1]

    r2_target = rule[5]
    r2_rel_type = rule[4]

    r3_source = rule[6]
    r3_rel_type = rule[7]
    r3_target = rule[8]

    triples = []

    # Search for variables where r1.target == r2.source
    for r1 in relations:
        for r2 in relations:
            if r1.source == r2.target:
                if r1.relation_type == r1_rel_type and r2.relation_type == r2_rel_type:
                    transitive = self._find_transitive(relations, r1.target, r2.source, rule)
                    if transitive:
                        triples.append([r1, r2, transitive])

    return triples

def _get_triples_target_equal(relations, rule):
    r1_source= rule[0]
    r1_rel_type = rule[1]

    r2_target = rule[5]
    r2_rel_type = rule[4]

    r3_source = rule[6]
    r3_rel_type = rule[7]
    r3_target = rule[8]

    triples = []

    # Search for variables where r1.target == r2.target
    for r1 in relations:
        for r2 in relations:
            if r1.target == r2.target:
                if r1.relation_type == r1_rel_type and r2.relation_type == r2_rel_type:
                    transitive = self._find_transitive(relations, r1.source, r2.source, rule)
                    if transitive:
                        triples.append([r1, r2, transitive])

    return triples

def _get_triples_source_equal(relations, rule):
    r1_target = rule[2]
    r1_rel_type = rule[1]
    r2_target = rule[5]
    r2_rel_type = rule[4]

    r3_source = rule[6]
    r3_rel_type = rule[7]
    r3_target = rule[8]

    triples = []

    # Search for variables with same source
    for r1 in relations:
        for r2 in relations:
            if r1.source == r2.source:
                if r1.relation_type == r1_rel_type and r2.relation_type == r2_rel_type:
                    transitive = _find_transitive(relations, r1.target, r2.target, rule)
                    if transitive:
                        triples.append([r1, r2, transitive])

    return triples

def _find_transitive(relations, source, target, rule):
    r3_rel_type = rule[7]

    for r in relations:
        if r.source == source and r.target == target and r.relation_type == r3_rel_type:
            return r
    else:
        return None

def get_number_of_misclassified_rels(triple):
    misclassified = 0

    for relation in triple:
        if relation.predicted_class != relation.relation_type:
            misclassified += 1

    return misclassified

data = Data()
system = System(data)

# Create features and apply feature selection
system.use_all_features()
system.use_feature_selection()
system.create_features()
system.train()
system.eval(quiet=True)

ee_zero_misclassified = 0
ee_one_misclassified = 0
ee_two_misclassified = 0
ee_three_misclassified = 0

et_zero_misclassified = 0
et_one_misclassified = 0
et_two_misclassified = 0
et_three_misclassified = 0

for text_obj in data.test.text_objects:
    # Get all unique triples of transitive relations in test data
    transitive_relations = get_transitives(text_obj.relations)

    # Check how many misclassified relations there are for every transitive relation
    for triple in transitive_relations:
        misclassified = get_number_of_misclassified_rels(triple)

        if triple[0].is_event_event() and triple[1].is_event_event():
            if misclassified == 0:
                ee_zero_misclassified += 1
            elif misclassified == 1:
                ee_one_misclassified += 1
            elif misclassified == 2:
                ee_two_misclassified += 1
            elif misclassified == 3:
                ee_three_misclassified += 1

        elif triple[0].is_event_timex() or triple[1].is_event_timex():
            if misclassified == 0:
                et_zero_misclassified += 1
            elif misclassified == 1:
                et_one_misclassified += 1
            elif misclassified == 2:
                et_two_misclassified += 1
            elif misclassified == 3:
                et_three_misclassified += 1

print ee_zero_misclassified
print ee_one_misclassified
print ee_two_misclassified
print ee_three_misclassified
print

print et_zero_misclassified
print et_one_misclassified
print et_two_misclassified
print et_three_misclassified
