class Relation:
    def __init__(self, lid, text_obj, source, target, relation_type):
        self.lid = lid
        self.parent_node = text_obj
        self.source_event = source
        self.target_event = target
        self.relation_type = relation_type
