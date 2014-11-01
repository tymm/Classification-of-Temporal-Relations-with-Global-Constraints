from parsexml.relation import Relation
from parsexml.relationtype import RelationType

class Complex_closure:
    def __init__(self, text_obj, transitives_of_transitives=False):
        """If transitives_of_transitives is True we will calculate all possible transitives. Otherwise it will only be returned direct transitives."""
        self.transitives_of_transitives = transitives_of_transitives
        self.text_obj = text_obj
        self.relations = text_obj.relations

    def get_complex_closure(self):
        if self.transitives_of_transitives:
            # Not yet implemented
            pass
        else:
            closure = self._generate_complex_closures(self.relations)
            return closure

    def _generate_complex_closures(self, relations):
        """Genereates closures like 'before && simultaneous => before' which have a form other than 'before && before => before'."""
        closures = []

        # A before B && B includes C => A before C
        rule = [RelationType.BEFORE, RelationType.INCLUDES, RelationType.BEFORE]
        closures += self._get_complex_closure_by_rule(rule, relations)

        # A before B && B simultaneous C => A before C
        rule = [RelationType.BEFORE, RelationType.SIMULTANEOUS, RelationType.BEFORE]
        closures += self._get_complex_closure_by_rule(rule, relations)

        # A includes B && B simultaneous C => A includes C
        rule = [RelationType.INCLUDES, RelationType.SIMULTANEOUS, RelationType.INCLUDES]
        closures += self._get_complex_closure_by_rule(rule, relations)

        # A simultaneous B && B before C => A before C
        rule = [RelationType.SIMULTANEOUS, RelationType.BEFORE, RelationType.BEFORE]
        closures += self._get_complex_closure_by_rule(rule, relations)

        # A simultaneous B && B includes C => A includes C
        rule = [RelationType.SIMULTANEOUS, RelationType.INCLUDES, RelationType.INCLUDES]
        closures += self._get_complex_closure_by_rule(rule, relations)

        return closures

    def _get_complex_closure_by_rule(self, rule, relations):
        closures = []

        AB = rule[0]
        BC = rule[1]
        AC = rule[2]

        for first_rel in relations:
            if first_rel.relation_type == AB:
                # We have the first part
                for second_rel in relations:
                    if second_rel.relation_type == BC and first_rel.target == second_rel.source:
                        # We have the second part
                        # Now we can create the closure between A and C
                        closure = Relation("closure", self.text_obj, first_rel.source, second_rel.target, AC)
                        closures.append(closure)

        return closures
