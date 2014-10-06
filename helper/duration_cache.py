import cPickle as pickle

class Duration_cache:
    def __init__(self):
        self.word_likelihoods = pickle.load(open("word_likelihoods.p", "rb"))
        self.infinitives = pickle.load(open("infinitives.p", "rb"))
