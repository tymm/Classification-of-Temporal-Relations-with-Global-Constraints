import cPickle as pickle

class Persistence:
    def __init__(self, file):
        self.file = file
        self.text_obj = None
        self._load_text_obj()

    def save(self, text_obj):
        self.text_obj = text_obj

        text_objs = self._load_text_objs()

        if text_objs:
            text_objs[self.file] = text_obj
            pickle.dump(text_objs, open("data.p", "wb"))
        else:
            text_objs = {}
            text_objs[self.file] = text_obj
            pickle.dump(text_objs, open("data.p", "wb"))

    def get_text_object(self):
        return self.text_obj

    def _load_text_objs(self):
        text_objs = None

        try:
            text_objs = pickle.load(open("data.p", "rb"))
        except IOError:
            pass

        return text_objs

    def _load_text_obj(self):
        text_objs = self._load_text_objs()

        try:
            self.text_obj = text_objs[self.file]
        except (TypeError, KeyError):
            self.text_obj = None
