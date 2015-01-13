from Data import Data
from System import System
from parsexml.relationtype import RelationType

def get_transitives(relations):
    triples = []

    # A before B && B before C => A before C
    rule = ["A", RelationType.BEFORE, "B", "B", RelationType.BEFORE, "C", "A", RelationType.BEFORE, "C"]
    triples += _get_triples_by_rule(relations, rule)

    # A before B && B includes C => A before C
    rule = ["A", RelationType.BEFORE, "B", "B", RelationType.INCLUDES, "C", "A", RelationType.BEFORE, "C"]
    triples += _get_triples_by_rule(relations, rule)

    # A before B && B simultaneous C => A before C
    rule = ["A", RelationType.BEFORE, "B", "B", RelationType.SIMULTANEOUS, "C", "A", RelationType.BEFORE, "C"]
    triples += _get_triples_by_rule(relations, rule)

    # A includes B && B includes C => A includes C
    rule = ["A", RelationType.INCLUDES, "B", "B", RelationType.INCLUDES, "C", "A", RelationType.INCLUDES, "C"]
    triples += _get_triples_by_rule(relations, rule)

    # A includes B && B simultaneous C => A includes C
    rule = ["A", RelationType.INCLUDES, "B", "B", RelationType.SIMULTANEOUS, "C", "A", RelationType.INCLUDES, "C"]
    triples += _get_triples_by_rule(relations, rule)

    # A simultaneous B && B before C => A before C
    rule = ["A", RelationType.SIMULTANEOUS, "B", "B", RelationType.BEFORE, "C", "A", RelationType.BEFORE, "C"]
    triples += _get_triples_by_rule(relations, rule)

    # A simultaneous B && B includes C => A includes C
    rule = ["A", RelationType.SIMULTANEOUS, "B", "B", RelationType.INCLUDES, "C", "A", RelationType.INCLUDES, "C"]
    triples += _get_triples_by_rule(relations, rule)

    # A simultaneous B && B simultaneous C => A simultaneous C
    rule = ["A", RelationType.SIMULTANEOUS, "B", "B", RelationType.SIMULTANEOUS, "C", "A", RelationType.SIMULTANEOUS, "C"]
    triples += _get_triples_by_rule(relations, rule)

    # Deduced
    # A simultaneous B && A before C => B before C
    rule = ["A", RelationType.SIMULTANEOUS, "B", "A", RelationType.BEFORE, "C", "B", RelationType.BEFORE, "C"]
    triples += _get_triples_by_rule(relations, rule)

    # A simultaneous B && A includes C => B includes C
    rule = ["A", RelationType.SIMULTANEOUS, "B", "A", RelationType.INCLUDES, "C", "B", RelationType.INCLUDES, "C"]
    triples += _get_triples_by_rule(relations, rule)

    # New (inverses)
    # A after B && B after C => A after C
    rule = ["A", RelationType.AFTER, "B", "B", RelationType.AFTER, "C", "A", RelationType.AFTER, "C"]
    triples += _get_triples_by_rule(relations, rule)

    # A after B && B includes C => A after C
    rule = ["A", RelationType.AFTER, "B", "B", RelationType.INCLUDES, "C", "A", RelationType.AFTER, "C"]
    triples += _get_triples_by_rule(relations, rule)

    # A after B && B simultaneous C => A after C
    rule = ["A", RelationType.AFTER, "B", "B", RelationType.SIMULTANEOUS, "C", "A", RelationType.AFTER, "C"]
    triples += _get_triples_by_rule(relations, rule)

    # A is_included B && B is_included C => A is_included C
    rule = ["A", RelationType.IS_INCLUDED, "B", "B", RelationType.IS_INCLUDED, "C", "A", RelationType.IS_INCLUDED, "C"]
    triples += _get_triples_by_rule(relations, rule)

    # A is_included B && B simultaneous C => A is_included C
    rule = ["A", RelationType.IS_INCLUDED, "B", "B", RelationType.SIMULTANEOUS, "C", "A", RelationType.IS_INCLUDED, "C"]
    triples += _get_triples_by_rule(relations, rule)

    # A is_included B && B after C => A after C
    rule = ["A", RelationType.IS_INCLUDED, "B", "B", RelationType.AFTER, "C", "A", RelationType.AFTER, "C"]
    triples += _get_triples_by_rule(relations, rule)

    # A is_included B && B before C => A before C
    rule = ["A", RelationType.IS_INCLUDED, "B", "B", RelationType.BEFORE, "C", "A", RelationType.BEFORE, "C"]
    triples += _get_triples_by_rule(relations, rule)

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
        return _get_triples_source_equal(relations, rule)
    elif r1_source == r2_target:
        return _get_triples_r1_source_r2_target_equal(relations, rule)
    elif r1_target == r2_target:
        return _get_triples_target_equal(relations, rule)
    elif r1_target == r2_source:
        return _get_triples_r1_target_r2_source_equal(relations, rule)

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
                    transitive = _find_transitive(relations, r1.target, r2.source, rule)
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
                    transitive = _find_transitive(relations, r1.source, r2.source, rule)
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

def get_number_of_miclassified_event_event_rels(triple):
    misclassified = 0

    for relation in triple:
        if relation.is_event_event() and relation.predicted_class != relation.relation_type:
            misclassified += 1

    return misclassified

def get_number_of_miclassified_event_timex_rels(triple):
    misclassified = 0

    for relation in triple:
        if relation.is_event_timex() and relation.predicted_class != relation.relation_type:
            misclassified += 1

    return misclassified

def get_number_of_event_event_rels(triple):
    n = 0
    for relation in triple:
        if relation.is_event_event():
            n += 1

    return n

def get_number_of_event_timex_rels(triple):
    n = 0
    for relation in triple:
        if relation.is_event_timex():
            n += 1

    return n

def get_global_model_triple(pairwise_triple):
    global_model_triple = []
    text_obj = pairwise_triple[0].parent

    for rel in pairwise_triple:
        for rel_optimized in text_obj.relations_plain_optimized:
            if rel.target == rel_optimized.target and rel.source == rel_optimized.source:
                global_model_triple.append(rel_optimized)

    return global_model_triple

def get_number_of_inconsistencies_solved_wrongly_by_global_model(subgraphs_with_potentially_improvements):
    n = 0

    for triple in subgraphs_with_potentially_improvements:
        gm_tripel = get_global_model_triple(triple)

        if triple[0].predicted_class != gm_tripel[0].relation_type or triple[1].predicted_class != gm_tripel[1].relation_type or triple[2].predicted_class != gm_tripel[2].relation_type:
            # There was exactly _one_ change from pairwise classification to global model in the subgraph
            if not (triple[0].relation_type == gm_tripel[0].relation_type and triple[1].relation_type == gm_tripel[1].relation_type and triple[2].relation_type == gm_tripel[2].relation_type):
                # The global model did not solve all misclassification - it exchanged a misclassificaton with another misclassification
                n += 1

    return n

def get_number_of_inconsistencies_solved_wrongly_by_global_model(subgraphs_with_potentially_improvements):
    rels = []

    for triple in subgraphs_with_potentially_improvements:
        gm_tripel = get_global_model_triple(triple)

        if triple[0].predicted_class != gm_tripel[0].relation_type or triple[1].predicted_class != gm_tripel[1].relation_type or triple[2].predicted_class != gm_tripel[2].relation_type:
            # There was exactly _one_ change from pairwise classification to global model in the subgraph
            if not (triple[0].relation_type == gm_tripel[0].relation_type and triple[1].relation_type == gm_tripel[1].relation_type and triple[2].relation_type == gm_tripel[2].relation_type):
                # The global model did not solve all misclassification - it exchanged a misclassificaton with another misclassification
                rels.append((triple, gm_tripel))

    return rels


def get_number_of_pairwise_classifier_mistakes_which_do_not_create_inconsistency(subgraphs_with_potentially_improvements):
    n = 0

    for triple in subgraphs_with_potentially_improvements:
        gm_tripel = get_global_model_triple(triple)

        if triple[0].predicted_class == gm_tripel[0].relation_type and triple[1].predicted_class == gm_tripel[1].relation_type and triple[2].predicted_class == gm_tripel[2].relation_type:
            n += 1

    return n

def get_triple_of_pairwise_classifier_mistakes_which_do_not_create_inconsistency(subgraphs_with_potentially_improvements):
    rels = []

    for triple in subgraphs_with_potentially_improvements:
        gm_tripel = get_global_model_triple(triple)

        if triple[0].predicted_class == gm_tripel[0].relation_type and triple[1].predicted_class == gm_tripel[1].relation_type and triple[2].predicted_class == gm_tripel[2].relation_type:
            rels.append(triple)

    return rels

data = Data()
system = System(data)

# Create features and apply feature selection
system.use_all_features()
system.use_feature_selection()
system.create_features()
system.train()

# Needs to be called to set relation.predicted_class
system.save_predictions_to_relations()
system.eval(quiet=True)

# Run global model
system.create_confidence_scores()
system.apply_global_model()

zero_misclassified = 0
one_misclassified = 0
two_misclassified = 0
three_misclassified = 0

wrong_ee = 0
wrong_et = 0
total_ee = 0
total_et = 0

# Subgraphs where exactly one misclassification happened by the pairwise classifier
subgraphs_with_potentially_improvements = []

for text_obj in data.test.text_objects:
    # Get all unique triples of transitive relations in test data
    transitive_relations = get_transitives(text_obj.relations)

    # Check how many misclassified relations there are for every transitive relation
    for triple in transitive_relations:
        misclassified = get_number_of_misclassified_rels(triple)

        wrong_ee += get_number_of_miclassified_event_event_rels(triple)
        total_ee += get_number_of_event_event_rels(triple)

        wrong_et += get_number_of_miclassified_event_timex_rels(triple)
        total_et += get_number_of_event_timex_rels(triple)

        if misclassified == 0:
            zero_misclassified += 1
        elif misclassified == 1:
            one_misclassified += 1
            # This is the only case where the global model can make improvements
            subgraphs_with_potentially_improvements.append(triple)
        elif misclassified == 2:
            two_misclassified += 1
        elif misclassified == 3:
            three_misclassified += 1

print "Total number of transitive subgraphs: " + str(zero_misclassified + one_misclassified + two_misclassified + three_misclassified)
print "Number of zero misclassified relations in transitive subgraphs: " + str(zero_misclassified)
print "Number of one misclassified relations in transitive subgraphs: " + str(one_misclassified)
print "Number of two misclassified relations in transitive subgraphs: " + str(two_misclassified)
print "Number of three misclassified relations in transitive subgraphs: " + str(three_misclassified)
print

print "% of misclassified event-event relations in transitive subgraphs: " + str(wrong_ee/float(total_ee))
print "% of misclassified event-timex relations in transitive subgraphs: " + str(wrong_et/float(total_et))
print

print "Number of transitive subgraphs where the pairwise classifier introduced one mistake which did not introduce a inconsistency: %s" % get_number_of_pairwise_classifier_mistakes_which_do_not_create_inconsistency(subgraphs_with_potentially_improvements)
print "Number of transitive subgraphs where the pairwise classifier changed one relation which did introduce a inconsistency and where the global model changed that inconsistency to another wrong relationtype: %s" % get_number_of_inconsistencies_solved_wrongly_by_global_model(subgraphs_with_potentially_improvements)
