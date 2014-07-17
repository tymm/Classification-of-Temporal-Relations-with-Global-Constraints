from Set import Set
from Feature import Feature

class TestSet(Set):
    def __init__(self, load=True, *corpora):
        Set.__init__(self, load, *corpora)
        self._create_all_relations_and_features()

    def _create_all_relations_and_features(self):
        """Creating all possible relations between all entities in all text objects of this set."""
        # Creating all possible relations and their features
        for text_obj in self.text_objects:
            text_obj.create_all_relations_and_features()


