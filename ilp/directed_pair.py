class Directed_Pair(object):
    def __init__(self, source, target, probabilities, classes):
        self.source = source
        self.target = target
        self.confidence_scores = self._map_proba_type(probabilities, classes)

    def _map_proba_type(self, probabilities, classes):
        """Map confidence score to class label."""
        m = {}
        for i, c in enumerate(classes):
            m[c] = probabilities[0][i]

        return m
