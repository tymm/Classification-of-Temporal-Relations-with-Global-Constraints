from parsexml.event import Event
from helper.tense_chooser import Tense_chooser
from helper.nlp_persistence import CouldNotFindGoverningVerb
from feature.exception import FailedProcessingFeature

class Tense(object):
    PRESENT = 0
    PAST = 1
    FUTURE = 2
    INFINITIVE = 3
    PRESPART = 4
    PASTPART = 5
    NONE = 6
    TIMEX = 7

    def __init__(self, relation, nlp_persistence_obj):
        self.relation = relation
        self.nlp_persistence_obj = nlp_persistence_obj
        self.source = self._get_source()
        self.target = self._get_target()

    @classmethod
    def get_length(cls):
        return 8

    def _get_source(self):
        source = self.relation.source

        if type(source) == Event:
            try:
                return self._determine_tense(source)
            except CouldNotFindGoverningVerb:
                return Tense.NONE
        else:
            return Tense.TIMEX

    def _get_target(self):
        target = self.relation.target

        if type(target) == Event:
            try:
                return self._determine_tense(target)
            except CouldNotFindGoverningVerb:
                return Tense.NONE
        else:
            return Tense.TIMEX

    def _determine_tense(self, event):
        text = event.tense

        if text == "PRESENT":
            return Tense.PRESENT
        elif text == "PAST":
            return Tense.PAST
        elif text == "FUTURE":
            return Tense.FUTURE
        elif text == "INFINITIVE":
            return Tense.INFINITIVE
        elif text == "PRESPART":
            return Tense.PRESPART
        elif text == "PASTPART":
            return Tense.PASTPART
        elif text == "NONE":
            if event.pos_xml == "NOUN" or event.pos_xml == "ADJECTIVE" or event.pos_xml == "PREPOSITION" or event.pos_xml == "PREP":
                # The event is noun, adjective or preposition
                # Let's return the tense of the governing verb
                governing_verb, index = self.nlp_persistence_obj.get_governing_verb(event)

                if governing_verb:
                    # Check if the governing verb has an entry with a tense (prefered method because we don't have to guess the tense then)
                    text_obj = self.relation.parent
                    governing_verb_as_event = text_obj.try_to_find_governing_verb_as_event(governing_verb, index, event)

                    if governing_verb_as_event and governing_verb_as_event.tense != Tense.NONE:
                        # We found the governing verb as an event
                        return self._determine_tense(governing_verb_as_event)
                    else:
                        # Let's guess the tense
                        tense_chooser = Tense_chooser(self.nlp_persistence_obj)
                        return tense_chooser.get_tense(event, governing_verb)
                else:
                    return Tense.NONE

            else:
                tense_chooser = Tense_chooser(self.nlp_persistence_obj)
                return tense_chooser.get_tense(event, event.text)
