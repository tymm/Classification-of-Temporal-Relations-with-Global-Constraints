from helper.tagger import StanfordNLP

class Timex(object):
    def __init__(self, tid, type, value, sentence, position_in_sentence):
        self.tid = tid
        self.type = type
        self.value = value
        self.sentence = sentence
        self.position_in_sentence = position_in_sentence
