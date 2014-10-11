from lxml import etree
from parsexml.sentence import Sentence
from parsexml.parser import Parser
from parsexml.relationtype import RelationType
from parsexml.relation import Relation
from Feature import Feature
from helper.output import Output
from parsexml.event import Event

class Text(object):
    def __init__(self, filename, test=False):
        self.filename = filename

        # Parse text
        parser = Parser(filename, self)

        self.text = parser.get_text()
        self.events = parser.get_events()
        self.timex = parser.get_timex()
        self.relations = parser.get_relations()

        # Only generate inversed and closured relations for training
        if not test:
            # Produce inversed relations
            self.relations += parser.get_inversed_relations()

            # Produce closure relations
            print "Create closures"
            self.relations += parser.get_closured_relations()

        self.text_structure = parser.get_text_structure()
        self.entities_order = parser.get_entities_order()

    def find_event_by_eiid(self, eiid):
        for event in self.events:
            if eiid in event.eiid:
                return event

        return None

    def find_event_by_eid(self, eid):
        for event in self.events:
            if event.eid == eid:
                return event

        return None

    def find_timex_by_tid(self, tid):
        for timex in self.timex:
            if timex.tid == tid:
                return timex

        return None

    def create_all_relations_and_features(self):
        """Creating all possible relations between all entities.

        Creating features here for performance.
        """
        all_relations = []

        feature = None

        for source in self.events + self.timex:
            for target in self.events + self.timex:
                for i, time in enumerate(RelationType()):
                    new_relation = Relation("all", self, source, target, time)

                    # We don't have the feature yet
                    if i == 0:
                        f = Feature(new_relation)
                        feature = f.get_feature()

                    if new_relation in self.relations:
                        continue
                    else:
                        new_relation.set_feature(feature)
                        all_relations.append(new_relation)

                feature = None

        self.relations = self.relations + all_relations

    def generate_output_tml_file(self):
        output = Output(self.filename)
        output.create_relations(self.relations)
        output.write()

    def try_to_find_governing_verb_as_event(self, governing_verb, index, event_in_same_sentence):

        sentence = event_in_same_sentence.sentence

        # Get events which are in the same sentence
        events_in_same_sentence = []
        for entity in self.text_structure.get_entities_by_sentence(sentence):
            if type(entity) == Event:
                events_in_same_sentence.append(entity)

        for event in events_in_same_sentence:
            if event.text == governing_verb and event.index == index:
                return event

        else:
            return None


class PosTagNotFound(Exception):
    def __init__(self, sentence, word):
        self.sentence = sentence
        self.word = word

    def __str__(self):
        return repr("Could not find POS tag for '" + self.word + "' in sentence: '" + self.sentence.text + "' in file " + self.sentence.filename)

class AuxNotFound(Exception):
    def __init__(self, aux):
        self.aux = aux

    def __str__(self):
        return repr("Could not find verb for aux \"" + self.aux + "\" in dependency relation")
