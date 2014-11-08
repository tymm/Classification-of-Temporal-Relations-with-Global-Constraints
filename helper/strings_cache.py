import cPickle as pickle

class Strings_cache:
    def __init__(self):
        tokens_set, lemmas_set = pickle.load(open("strings.p", "rb"))
        self.tokens = list(tokens_set)
        self.lemmas = list(lemmas_set)
