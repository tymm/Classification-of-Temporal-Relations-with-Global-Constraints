from TrainingSet import TrainingSet
from TestSet import TestSet
import cPickle as pickle
import os.path

class Data:
    def __init__(self, reload=False):
        self.FILENAME_CACHE = "data.p"

        if reload or not os.path.isfile(self.FILENAME_CACHE):
            self._load_new()
        else:
            try:
                self.training, self.test = pickle.load(open(self.FILENAME_CACHE, "rb"))
            except (IOError, EOFError):
                print "Corrupt " + self.FILENAME_CACHE + "! Reload data and write new cache."
                self._load_new()

    def _load_new(self):
        self.training = TrainingSet(False, "data/training/TE3-Silver-data/", "data/training/TBAQ-cleaned/AQUAINT/", "data/training/TBAQ-cleaned/TimeBank/")
        self.test = TestSet(False, "data/test/te3-platinum/")

        # Write to cache
        pickle.dump((self.training, self.test), open(self.FILENAME_CACHE, "wb"), protocol=-1)
