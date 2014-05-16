from parsexml.relation import Relation
from parsexml.relationtype import RelationType

class Closure:
    def __init__(self, text_obj, relation_type):
        self.text_obj = text_obj
        self.relation_type = relation_type
        self.new_relations = None
        self._generate_closure_relations()

    def get_closure_relations(self):
        return self.new_relations

    def _generate_closure_relations(self):
        """Generate new relations through partial temporal closure.

        Returns new generated relations for all events and timex known to the Parser object.
        """
        new_relations = []
        all_events_or_timex = self.text_obj.events + self.text_obj.timex

        for event_or_timex in all_events_or_timex:
            relations = self.text_obj.relations + new_relations
            tmp = self._generate_closure_relations_for_one(event_or_timex)
            if tmp:
                new_relations = new_relations + tmp

        self.new_relations = new_relations

    def _generate_closure_relations_for_one(self, a):
        closure_relations = []
        # Get events or timex which are connected to a over transitivity
        closures = self._get_closures(a)

        if closures:
            for b in closures:
                if not self._is_relation(a, b):
                    # Create new relation
                    closure_rel = Relation("closure", self.text_obj, a, b, self.relation_type)
                    closure_relations.append(closure_rel)
                    # Add this new relation also to the set of relations we are working with to use the new information in further decisions
                    self.text_obj.append_relation(closure_rel)

            return closure_relations
        else:
            return

    def _is_relation(self, source, target):
        for relation in self.text_obj.relations:
            if relation.source == source and relation.target == target:
                return True

        return False

    def _get_closures(self, source):
        closures = self._find_all_targets_with_source(source)

        if not closures:
            return
        else:
            for target in closures:
                deeper = self._get_closures(target)
                if deeper:
                    closures = closures + deeper

            return closures

    def _find_all_targets_with_source(self, source):
            bucket = []
            for relation in self.text_obj.relations:
                if relation.source == source and relation.relation_type == self.relation_type:
                    bucket.append(relation.target)

            return bucket
