from TrainingSet import TrainingSet
from TestSet import TestSet
import cPickle as pickle
import os.path

class Data:
    def __init__(self, inverse=False, closure=False, best_settings=True):
        self.inverse = inverse
        self.closure = closure
        # Overrides self.closure and self.inverse and leads to inversing only event-event relations (which is the best setting found)
        self.best_settings = best_settings

        self._load_new()

    def _load_new(self):
        self.training = TrainingSet(True, self.closure, self.best_settings, "data/training/TBAQ-cleaned/AQUAINT/", "data/training/TBAQ-cleaned/TimeBank/")
        self.test = TestSet("data/test/te3-platinum/")
