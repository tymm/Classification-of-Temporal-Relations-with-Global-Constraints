from parsexml.event import Event
from helper.nlp_persistence import CouldNotFindGoverningVerb
from feature.exception import FailedProcessingFeature

class Aspect(object):
    NONE = 0 # Indefinite
    PROGRESSIVE = 1
    PERFECTIVE = 2
    PERFECTIVE_PROGRESSIVE = 3
    UNKNOWN = 4
    TIMEX = 5

    def __init__(self, relation, nlp_persistence_obj):
        self.relation = relation
        self.nlp_persistence_obj = nlp_persistence_obj
        self.source = self._get_source()
        self.target = self._get_target()

    @classmethod
    def get_length(cls):
        return 6

    def _get_source(self):
        source = self.relation.source

        if type(source) == Event:
            try:
                aspect = self._determine_aspect(source)
                return aspect
            except CouldNotFindGoverningVerb:
                raise FailedProcessingFeature("Aspect")
        else:
            return Aspect.TIMEX

    def _get_target(self):
        target = self.relation.target

        if type(target) == Event:
            try:
                return self._determine_aspect(target)
            except CouldNotFindGoverningVerb:
                raise FailedProcessingFeature("Aspect")
        else:
            return Aspect.TIMEX

    def _determine_aspect(self, event):
        text = event.aspect

        if event.pos_xml == "NOUN" or event.pos_xml == "ADJECTIVE" or event.pos_xml == "PREPOSITION" or event.pos_xml == "PREP":
            # The event is noun, adjective or preposition
            # Let's return the aspect of the governing verb
            governing_verb = self.nlp_persistence_obj.get_governing_verb(event)

            if governing_verb is not None:
                # Check if the governing verb has an entry with a aspect(prefered method because we don't have to guess the aspect then)
                text_obj = self.relation.parent
                governing_verb_as_event = text_obj.try_to_find_governing_verb_as_event(governing_verb, event)

                if governing_verb_as_event:
                    # We found the governing verb as an event
                    return self._determine_aspect(governing_verb_as_event)
                else:
                    return Aspect.UNKNOWN
            else:
                return Aspect.UNKNOWN
        elif text == "PROGRESSIVE":
            return Aspect.PROGRESSIVE
        elif text == "PERFECTIVE":
            return Aspect.PERFECTIVE
        elif text == "PERFECTIVE_PROGRESSIVE":
            return Aspect.PERFECTIVE_PROGRESSIVE
        elif text == "NONE":
            return Aspect.NONE
