from nltk import word_tokenize
from parsexml.fakesentence import FakeSentence

class Tense_chooser:
    PRESENT = 0
    PAST = 1
    FUTURE = 2
    INFINITIVE = 3
    PRESPART = 4
    PASTPART = 5
    NONE = 6

    def __init__(self, nlp_persistence_obj):
        self.nlp_persistence_obj = nlp_persistence_obj

    def get_tense(self, event, verb):
        """The argument event must be an event in the same sentence as the verb text we want to get the tense for."""
        sentence = event.sentence

        tags = self.nlp_persistence_obj.find_all_verb_tags(sentence, verb)

        if self.is_Present(tags):
            return self.PRESENT
        elif self.is_Past(tags):
            return self.PAST
        elif self.is_Future(tags):
            return self.FUTURE
        else:
            return self.NONE

    def get_tense_only_for_tests(self, sentence, verb):
        """This is basically the same as get_tense() and it's only purpose is for testing."""
        fake_sentence = FakeSentence(sentence)

        tags = self.nlp_persistence_obj.find_all_verb_tags(fake_sentence, verb)

        if self.is_Present(tags):
            return self.PRESENT
        elif self.is_Past(tags):
            return self.PAST
        elif self.is_Future(tags):
            return self.FUTURE
        else:
            return self.NONE


    def is_Present(self, tags):
        if "VBZ" == tags[0]:
            return True
        else:
            return False

    def is_Past(self, tags):
        if "VBD" == tags[0]:
            return True
        else:
            return False

    def is_Future(self, tags):
        if "MD" == tags[0]:
            return True
        else:
            return False

    def is_Infinitive(self, tags):
        pass

    def is_PresentParticiple(self, tags):
        pass

    def is_PastParticiple(self, tags):
        pass
