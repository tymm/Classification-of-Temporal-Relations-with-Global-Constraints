from Set import Set
from Feature import Feature
from feature.exception import FailedProcessingFeature

class TrainingSet(Set):
    def __init__(self, inverse=False, closure=False, best_settings=True, *corpora):
        Set.__init__(self, inverse, closure, best_settings, *corpora)
