from helper.tagger import StanfordNLP

class Event(object):
    def __init__(self, eid, eiid, text_obj, text, sentence, position_in_sentence, e_class, tense, aspect, polarity, pos, modality):
        self.eid = eid
        self.eiid = [eiid]
        self.parent = text_obj
        self.text = text
        self.sentence = sentence
        self.position_in_sentence = position_in_sentence
        # self.pos = self._get_pos()
        self.pos = "NONE"

        # As definied in xml data
        self.e_class = e_class
        self.tense = tense
        self.aspect = aspect
        self.polarity = polarity
        self.pos_xml = pos
        self.modality = modality

    def __hash__(self):
        return hash(self.parent.filename + str(self.eid) + str(self.eiid))

    def __str__(self):
        return u"Event Object: eid: %s eiid: %s text: %s" % (self.eid, self.eiid, self.text)

    def _get_pos(self):
        s = StanfordNLP()
        pos_tag = s.parse(self.sentence, self.position_in_sentence)
        return pos_tag
