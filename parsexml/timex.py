from helper.tagger import StanfordNLP

class Timex(object):
    def __init__(self, tid, type, value, text, sentence, position_in_sentence, is_dct, text_obj):
        self.tid = tid
        self.type = type
        self.value = value
        self.text = text
        self.sentence = sentence
        self.position_in_sentence = position_in_sentence
        self.is_dct = is_dct
        self.parent = text_obj

    def __str__(self):
        return u"Timex Object: tid: %s text: %s" % (self.tid, self.text)

    def __hash__(self):
        return hash(self.parent.filename + str(self.tid) + self.text)
