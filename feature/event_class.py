from parsexml.event import Event

class Event_class(object):
    def __init__(self, relation):
        self.relation = relation
        self.classes = ["PERCEPTION", "I_STATE", "ASPECTUAL", "REPORTING", "I_ACTION", "STATE", "OCCURRENCE"]

    def get_length(self):
        # +1 for N/A
        return len(self.classes) + 1

    def get_index_source(self):
        if type(self.relation.source) == Event:
            return self._get_index(self.relation.source.e_class)
        else:
            # Return N/A value
            return self.get_length()

    def get_index_target(self):
        if type(self.relation.target) == Event:
            return self._get_index(self.relation.target.e_class)
        else:
            # Return N/A value
            return self.get_length()

    def _get_index(self, string):
        try:
            return self.classes.index(string)
        except ValueError:
            print "Unkown index in Class feature: " + string
