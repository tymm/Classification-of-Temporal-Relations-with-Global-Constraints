from collections import OrderedDict
from parsexml.sentence import Sentence
from parsexml.fakesentence import FakeSentence
from lxml import etree
import nltk.data

class Text_structure:
    def __init__(self, filename, parser_obj):
        self.filename = filename
        self.sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        self.parser_obj = parser_obj

        # {Sentence: [Event, Timex, ...]
        self.structure = OrderedDict()

        self._entities_ordered = []
        self._entity_nodes_ordered = []

        self._build_entities_ordered()
        self._build_structure()

    def get_entities_ordered(self):
        return self._entities_ordered

    def get_structure(self):
        return self.structure

    def print_structure(self):
        print "----Structure start----"
        for sentence, entities in self.structure.items():
            print "---Sentence start---"
            print sentence.text
            for entity in entities:
                print entity.text

            print "---Sentence end---"
            print
        print "----Structure end----"
        print

    def get_sentence(self, entity):
        for sentence, entities in self.structure.items():
            if entity in entities:
                return sentence

        else:
            return None

    def get_sentence_distance(self, entity_one, entity_two):
        sentences = self.structure.values()

        position_one = None
        position_two = None

        for sentence in sentences:
            if entity_one in sentence or entity_two in sentence:
                # Start counting
                if entity_one in sentence and entity_two in sentence:
                    # Both entities are in the same sentence
                    return 0

                if entity_one in sentence:
                    position_one = sentences.index(sentence)

                if entity_two in sentence:
                    position_two = sentences.index(sentence)

        try:
            difference = abs(position_one - position_two)
        except TypeError:
            # One or both entities are not in any sentence
            difference = None

        return difference

    def _get_entity_by_node(self, entity_node):
        eid = entity_node.get("eid")

        if eid:
            # It's an event
            entity = self.parser_obj.find_event_by_eid(self.parser_obj.get_events(), eid)
        else:
            # It's a timex
            tid = entity_node.get("tid")
            entity = self.parser_obj.find_timex_by_tid(tid)

        return entity

    def _build_entities_ordered(self):
        tree = etree.parse(self.filename)
        root_node = tree.getroot()

        # Also look for document creation time (dct) information
        dct_node = root_node.find("DCT")
        dct_timex_node = dct_node[0]
        dct_timex = self._get_entity_by_node(dct_timex_node)

        self._entities_ordered.append(dct_timex)
        self._entity_nodes_ordered.append(dct_timex_node)

        text_node = root_node.find("TEXT")

        # Problem: Some entities in <TEXT></TEXT> have more than one entity in <MAKEINSTANCE></MAKEINSTANCE>
        # Solution: Handle this problem elsewhere (for example directly in feature/sentence_distance.py)
        for entity_node in text_node:
            # Since we are only interested in the structure of the text here, just get one entity even if there are more than one for entity_node
            entity = self._get_entity_by_node(entity_node)

            self._entities_ordered.append(entity)
            self._entity_nodes_ordered.append(entity_node)

    def _build_structure(self):
        for entity_node in self._entity_nodes_ordered:
            # Problem: Not all sentences have an entity
            sentence = Sentence(entity_node, self.parser_obj.text_obj.filename)
            # Get entity object by lxml object
            entity = self._get_entity_by_node(entity_node)

            # If sentence not yet in self.structure, we know that entity is the first entity of this sentence
            if sentence not in self.structure:
                self.structure.update({sentence: [entity]})
            # Sentence is already known. Let's append this entity to the already known sentence
            else:
                self.structure[sentence].append(entity)

        # Add sentences which don't have entities
        self._add_sentences_without_entities()

    def _add_sentences_without_entities(self):
        """Strategy:
        Get the whole text
        Split the whole text into sentences
        If a sentence is not yet in self.structure then add it to the right position
        """
        all_text = self._get_all_text()

        # Split into single sentences
        sentences = self.sent_detector.tokenize(all_text)

        # Create FakeSentence objects for being able to compare with Sentence objects
        fake_sentences = []
        for sentence in sentences:
            fake_sentences.append(FakeSentence(sentence))

        index_of_last_real_sentence = 0
        for fakesentence in fake_sentences:
            if fakesentence in self.structure.keys():
                # This sentence is already in the structure; it contains an entity
                index_of_last_real_sentence = self.structure.keys().index(fakesentence)
            else:
                # This sentence is not yet in the structure
                # Append it after position to self.structure
                self._append_fakesentence_to_structure_after_position(fakesentence, index_of_last_real_sentence)

    def _get_all_text(self):
        tree = etree.parse(self.filename)
        root_node = tree.getroot()

        text_node = root_node.find("TEXT")

        # Get the very beginning of the text
        text = ""
        if text_node.text:
            text = text_node.text

        # Getting the rest
        try:
            entity = text_node[0]
        except IndexError:
            # There seems to be no events; True for test files
            return text

        while entity is not None:
            text = text + entity.text + entity.tail
            entity = entity.getnext()

        return text

    def _append_fakesentence_to_structure_after_position(self, fakesentence, position):
        """Append at position. If there are FakeSentence objects after position then put item at the end of them and before the next real Sentence object."""
        # Convert to list
        l = self.structure.items()

        position_to_insert = self._find_position_to_insert_sentence(position)

        # Insert (item, []) to be consistent with the definition of structure
        l.insert(position_to_insert, (fakesentence, []))

        # Update structure
        self.structure = OrderedDict(l)

    def _find_position_to_insert_sentence(self, starting_position):
        # Search for first non FakeSentence objects after position
        position_to_insert = None

        # List of sentences (entities are not interesting here)
        list_of_sentences = self.structure.keys()

        for sentence in list_of_sentences[(starting_position+1):]:
            if type(sentence) is Sentence:
                position_to_insert = list_of_sentences.index(sentence)
                return position_to_insert

        return len(list_of_sentences)
