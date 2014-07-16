from Set import Set
from Feature import Feature

class TestSet(Set):
    def __init__(self, load=True, *corpora):
        Set.__init__(self)
