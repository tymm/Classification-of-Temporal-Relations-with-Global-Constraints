from Set import Set
from Feature import Feature
from feature.exception import FailedProcessingFeature

class TrainingSet(Set):
    def __init__(self, inverse=True, closure=True, *corpora):
        # No full closure for training, since this is what was done in the reference paper
        Set.__init__(self, inverse, closure, False, *corpora)
