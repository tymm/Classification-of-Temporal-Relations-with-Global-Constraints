from TrainingSet import TrainingSet
from TestSet import TestSet

class Data:
    def __init__(self):
        self.training = TrainingSet(False, "data/training/TE3-Silver-data/", "data/training/TBAQ-cleaned/AQUAINT/", "data/training/TBAQ-cleaned/TimeBank/")
        self.test = TestSet(False, "data/test/te3-platinum/")
