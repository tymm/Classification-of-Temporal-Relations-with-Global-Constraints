class Relation:
    def __init__(self, lid, text_obj, source_event_obj, target_event_obj, relation_type):
        self.lid = lid
        self.parent_node = text_obj
        self.source_event = source_event_obj
        self.target_event = target_event_obj
        self.relation_type = relation_type
