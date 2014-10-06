from Set import Set
from Feature import Feature
from feature.exception import FailedProcessingFeature

class TrainingSet(Set):
    def __init__(self, load=True, *corpora):
        Set.__init__(self, load, False, *corpora)
