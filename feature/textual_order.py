class Textual_order:
    def __init__(self, relation):
        self._text_obj = relation.parent
        self._a = relation.source
        self._b = relation.target

    def a_before_b(self):
        order = self._text_obj.entities_order
        if order.index(self._a) < order.index(self._b):
            return True
        else:
            return False
