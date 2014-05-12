class Relation:
    def __init__(self, text_obj, source, target, relation_type):
        self.parent_node = text_obj
        self.source_event = source
        self.target_event = target
        self.relation_type = relation_type
