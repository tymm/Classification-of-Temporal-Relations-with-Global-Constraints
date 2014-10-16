import cPickle as pickle

class Strings_cache:
    def __init__(self):
        self.tokens, self.lemmas = pickle.load(open("strings.p", "rb"))
