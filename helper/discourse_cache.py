import cPickle as pickle

class Discourse_cache:
    def __init__(self):
        self.data = pickle.load(open("discourse_cache.p", "rb"))
