from parsexml.event import Event
from helper.tense_chooser import Tense_chooser

class Tense(object):
    PRESENT = 0
    PAST = 1
    FUTURE = 2
    INFINITIVE = 3
    PRESPART = 4
    PASTPART = 5
    NONE = 6

    def __init__(self, relation, nlp_persistence_obj):
        self.relation = relation
        self.nlp_persistence_obj = nlp_persistence_obj
        self.source = self._get_source()
        self.target = self._get_target()

    @classmethod
    def get_length(cls):
        return 7

    def _get_source(self):
        source = self.relation.source

        if type(source) == Event:
            return self._determine_tense(source)
        else:
            return Tense.NONE

    def _get_target(self):
        target = self.relation.target

        if type(target) == Event:
            return self._determine_tense(target)
        else:
            return Tense.NONE

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
                governing_verb = self._get_governing_verb(event)

                if governing_verb is not None:
                    # Check if the governing verb has an entry with a tense (prefered method because we don't have to guess the tense then)
                    governing_verb_as_event = self._try_to_find_governing_verb_as_event(governing_verb, event)

                    if governing_verb_as_event and governing_verb_as_event.tense != Tense.NONE:
                        # We found the governing verb as an event
                        return self._determine_tense(governing_verb_as_event)
                    else:
                        # Let's guess the tense
                        # return Tense_chooser.get_tense(governing_verb)
                        return Tense.NONE
                else:
                    return Tense.NONE
            else:
                return Tense.NONE

    def _try_to_find_governing_verb_as_event(self, governing_verb, close_event):
        text_obj = close_event.parent
        entities = close_event.parent.entities_order

        verb = None
        aux = None
        if len(governing_verb.split()) == 1:
            # no aux
            verb = governing_verb
        else:
            # aux and verb
            aux = governing_verb.split()[0]
            verb = governing_verb.split()[1]

        # Search for governing verb in entities
        indexes = []
        for entity in entities:
            if entity is None:
                print entities
                print text_obj.filename
            if aux:
                if entity.text == aux + " " + verb or entity.text == verb:
                    indexes.append(entities.index(entity))
            else:
                if entity.text == verb:
                    indexes.append(entities.index(entity))

        # Choose the entity which is the closest to the event
        if len(indexes) != 0:
            close_event_index = entities.index(close_event)

            diff_smallest = indexes[0]
            index_smallest = None
            for index in indexes:
                diff = abs(index - close_event_index)
                if diff_smallest >= diff:
                    diff_smallest = diff
                    index_smallest = index

            return entities[index_smallest]

        else:
            return None

    def _get_governing_verb(self, event):
        sentence = event.sentence

        # info = [verb, aux, pos verb, pos aux]
        info = sentence.get_info_on_governing_verb(event.text, self.nlp_persistence_obj)

        if info is None:
            return None
        elif info[1]:
           return info[1] + " " + info[0]
        else:
           return info[0]
