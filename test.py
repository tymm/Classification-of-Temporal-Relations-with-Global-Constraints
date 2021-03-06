import unittest

from parsexml.text import Text
from parsexml.relation import Relation
from parsexml.parser import Parser
from Feature import Feature as Features
from parsexml.fakesentence import FakeSentence
from parsexml.sentence import Sentence
from lxml import etree
from helper.nlp_persistence import Nlp_persistence
from feature.tense import Tense
from helper.tense_chooser import Tense_chooser
from Set import Set
from parsexml.event import Event
from feature.dependency_order import Dependency_order
from parsexml.relationtype import RelationType
from System import System
from TrainingSet import TrainingSet
from TestSet import TestSet
from helper.duration_cache import Duration_cache
from Constraints import Constraints
from ilp.variable import Variable
from ilp.directed_pair import Directed_Pair

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class NLP_cache(object):
    """Use this singleton so that not every test case has to reload the nlp cache."""
    __metaclass__ = Singleton

    # Set up the CoreNLP persistence layer
    nlp_layer = Nlp_persistence(fallback=True)
    nlp_layer.load()

class TextStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        filename = "data/training/TBAQ-cleaned/TimeBank/ABC19980304.1830.1636.tml"
        cls.text_obj = Text(filename)

        cls.all_data = Set(False, "data/training/TE3-Silver-data/", "data/training/TBAQ-cleaned/AQUAINT/", "data/training/TBAQ-cleaned/TimeBank/", "data/test/te3-platinum/")

    def test_AreThereNoNonesInEntitiesOrder(self):
        for text_obj in self.all_data.text_objects:
            for entity in text_obj.entities_order:
                self.assertNotEqual(entity, None)

    def test_GetAnEntitiesSentenceByEnitity(self):
        entities_ordered = self.text_obj.text_structure.get_entities_ordered()

        # Get sentence of event e1
        sentence = self.text_obj.text_structure.get_sentence(entities_ordered[2])

        self.assertEqual(sentence, FakeSentence("Finally today, we learned that the space agency has finally taken a giant leap forward."))

    def test_GetAnEntitiesSentenceByEnitity_2(self):
        entities_ordered = self.text_obj.text_structure.get_entities_ordered()

        # Get sentence of timex t33
        sentence = self.text_obj.text_structure.get_sentence(entities_ordered[7])

        self.assertEqual(sentence, FakeSentence("Air Force Lieutenant Colonel Eileen Collins will be named commander of the Space Shuttle Columbia for a mission in December."))

    def test_RightOrderOfEntities(self):
        entities_ordered = self.text_obj.text_structure.get_entities_ordered()

        self.assertEqual(entities_ordered[0].tid, "t0")
        self.assertEqual(entities_ordered[1].tid, "t32")
        self.assertEqual(entities_ordered[2].eid, "e1")
        self.assertEqual(entities_ordered[3].eid, "e2")
        self.assertEqual(entities_ordered[4].eid, "e3")
        self.assertEqual(entities_ordered[5].eid, "e37")
        self.assertEqual(entities_ordered[6].eid, "e38")
        self.assertEqual(entities_ordered[7].tid, "t33")
        self.assertEqual(entities_ordered[8].eid, "e40")
        self.assertEqual(entities_ordered[9].eid, "e41")
        self.assertEqual(entities_ordered[10].tid, "t34")
        self.assertEqual(entities_ordered[11].eid, "e6")
        self.assertEqual(entities_ordered[12].eid, "e7")
        self.assertEqual(entities_ordered[13].eid, "e254")
        self.assertEqual(entities_ordered[14].tid, "t55")
        self.assertEqual(entities_ordered[15].eid, "e68")
        self.assertEqual(entities_ordered[16].eid, "e44")
        self.assertEqual(entities_ordered[17].eid, "e10")
        self.assertEqual(entities_ordered[18].eid, "e20")
        self.assertEqual(entities_ordered[19].tid, "t36")
        self.assertEqual(entities_ordered[20].eid, "e51")
        self.assertEqual(entities_ordered[21].eid, "e22")
        self.assertEqual(entities_ordered[22].eid, "e52")
        self.assertEqual(entities_ordered[23].eid, "e23")
        self.assertEqual(entities_ordered[24].eid, "e24")
        self.assertEqual(entities_ordered[25].eid, "e25")
        self.assertEqual(entities_ordered[26].eid, "e26")
        self.assertEqual(entities_ordered[27].eid, "e27")
        self.assertEqual(entities_ordered[28].eid, "e28")
        self.assertEqual(entities_ordered[29].eid, "e30")

    def test_RightOrderOfSentences(self):
        structure = self.text_obj.text_structure.get_structure()

        sentences = [sentence for sentence in structure]

        self.assertEqual(sentences[0], FakeSentence("19980304"))
        self.assertEqual(sentences[1], FakeSentence("Finally today, we learned that the space agency has finally taken a giant leap forward."))
        self.assertEqual(sentences[2], FakeSentence("Air Force Lieutenant Colonel Eileen Collins will be named commander of the Space Shuttle Columbia for a mission in December."))
        self.assertEqual(sentences[3], FakeSentence("Colonel Collins has been the co-pilot before, but this time she's the boss."))
        self.assertEqual(sentences[4], FakeSentence("Here's ABC's Ned Potter."))
        self.assertEqual(sentences[5], FakeSentence("Even two hundred miles up in space, there has been a glass ceiling."))
        self.assertEqual(sentences[6], FakeSentence("It wasn't until twenty years after the first astronauts were chosen that NASA finally included six women, and they were all scientists, not pilots."))
        self.assertEqual(sentences[7], FakeSentence("No woman has actually been in charge of a mission until now."))
        self.assertEqual(sentences[8], FakeSentence("Just the fact that we're doing the job that we're doing makes us role models."))
        self.assertEqual(sentences[9], FakeSentence("That was Eileen Collins, after she flew as the first ever co-pilot."))
        self.assertEqual(sentences[10], FakeSentence("Being commander is different."))
        self.assertEqual(sentences[11], FakeSentence("It means supervising the rest of the crew in training and leading them in flight."))
        self.assertEqual(sentences[12], FakeSentence("It is, in short, the kind of management job many American women say they've had to fight for."))
        self.assertEqual(sentences[13], FakeSentence("In space, some say female pilots were held up until now by the lack of piloting opportunities for them in the military."))
        self.assertEqual(sentences[14], FakeSentence("Once Colonel Collins was picked as a NASA astronaut, she followed a normal progression within NASA."))
        self.assertEqual(sentences[15], FakeSentence("Nobody hurried her up."))
        self.assertEqual(sentences[16], FakeSentence("No one held her back."))
        self.assertEqual(sentences[17], FakeSentence("Many NASA watchers say female astronauts have become part of the agency's routine."))
        self.assertEqual(sentences[18], FakeSentence("But they still have catching up to do two hundred and thirty four Americans have flown in space, only twenty six of them women."))
        self.assertEqual(sentences[19], FakeSentence("Ned Potter, ABC News."))

class SentenceExtraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        filename = "data/training/TBAQ-cleaned/TimeBank/wsj_1003.tml"
        filename_second = "data/training/TE3-Silver-data/AFP_ENG_19970425.0504.tml"
        filename_third = "data/training/TE3-Silver-data/AFP_ENG_20061224.0147.tml"
        filename_fourth = "data/training/TE3-Silver-data/AFP_ENG_20051210.0156.tml"
        filename_fifth = "data/training/TE3-Silver-data/XIN_ENG_20051107.0244.tml"

        cls.text_obj = Text(filename)
        cls.text_obj_second = Text(filename_second)
        cls.text_obj_third = Text(filename_third)
        cls.text_obj_fourth = Text(filename_fourth)
        cls.text_obj_fifth = Text(filename_fifth)

        cls.sentences = [s for s in cls.text_obj.text_structure.get_structure()]
        cls.sentences_second = [s for s in cls.text_obj_second.text_structure.get_structure()]
        cls.sentences_third = [s for s in cls.text_obj_third.text_structure.get_structure()]
        cls.sentences_fourth = [s for s in cls.text_obj_fourth.text_structure.get_structure()]
        cls.sentences_fifth = [s for s in cls.text_obj_fifth.text_structure.get_structure()]

    def test_CheckForRightSentenceBorders(self):
        self.assertEqual(self.sentences[1], FakeSentence("Bethlehem Steel Corp., hammered by higher costs and lower shipments to key automotive and service-center customers, posted a 54% drop in third-quarter profit."))
        self.assertEqual(self.sentences[2], FakeSentence("Separately, two more of the nation's top steelmakers -- Armco Inc. and National Intergroup Inc. -- reported lower operating earnings in their steel businesses, marking what is generally believed to be the end of a two-year boom in the industry."))
        self.assertEqual(self.sentences[3], FakeSentence("Wall Street analysts expect the disappointing trend to continue into the fourth quarter and through at least the first two quarters of 1990, when the industry will increasingly see the effect of price erosion in major product lines, such as rolled sheet used for cars, appliances and construction."))
        self.assertEqual(self.sentences[4], FakeSentence("\"It doesn't bode well for coming quarters,\" said John Jacobson, who follows the steel industry for AUS Consultants."))
        self.assertEqual(self.sentences[5], FakeSentence("In fact, he thinks several steelmakers will report actual losses through the third quarter of 1990."))
        self.assertEqual(self.sentences[6], FakeSentence("Bethlehem, the nation's second largest steelmaker, earned $46.9 million, or 54 cents a share."))

        self.assertEqual(self.sentences_second[3], FakeSentence("\"Today, everyone knows that Angolan troops are attacking Zaire for no reason and without declaring war,\" the statement said."))
        self.assertEqual(self.sentences_second[4], FakeSentence("Angolan troops were also in the area of Tshipaka, in Western Kasai province, a city some 650 kilometres (400 miles) southeast of the capital Kinshasa which Kabila's forces said Wednesday they had captured."))
        self.assertEqual(self.sentences_second[5], FakeSentence("According to the presidency statement the Kinshasa authorities will raise the Angolan incursions with the United Nations, and ask UN envoy Alioune Blondin Beye to visit the zones currently occupied by Angolan forces."))
        self.assertEqual(self.sentences_third[16], FakeSentence("The United Arab Emirates is to transfer 30 million dollars to the Palestinian Authority \"to help reduce the suffering of the Palestinian people,\" the official WAM news agency said."))
        self.assertEqual(self.sentences_fourth[4], FakeSentence("\"Nothing could justify Security Council measures against Syria,\" he said, adding that \"Syria is innocent of this crime.\""))
        print self.sentences_fifth[10]
        self.assertEqual(self.sentences_fifth[10], FakeSentence("According to the Russian media, the rallies and demonstrations organized by the Russian communists and the left parties were also held on Monday in other regions and cities, such as St. Petersburg, Krasnojarsk, Ulyanovsk, Kurgan, Kirov and Tula."))

class Feature(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        filename = "data/training/TBAQ-cleaned/TimeBank/ABC19980304.1830.1636.tml"
        cls.text_obj = Text(filename)

        cls.features = []

        for relation in cls.text_obj.relations:
            f = Features(relation, None, None, None, [])
            cls.features.append(f)

    def test_SentenceDistance(self):
        for feature in self.features:
            if feature.get_sentence_distance()[0] == None:
                print feature.relation.source
                print feature.relation.target
            self.assertNotEqual(feature.get_sentence_distance()[0], None)

class GoverningVerb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        filename = "data/training/TBAQ-cleaned/TimeBank/ABC19980304.1830.1636.tml"

        # Get a node a Sentence object can parse from
        tree = etree.parse(filename)
        root_node = tree.getroot()

        # Arguments for Sentence
        event_node = root_node.xpath("//EVENT")[0]

        # Sentence contains the following text:
        # "Finally today, we learned that the space agency has finally taken a giant leap forward."
        # The event we have is "learned"
        cls.sentence = Sentence(event_node, filename)

        cls.sentence2 = FakeSentence("Saudi authorities, who have been fighting a wave of violence by suspected Al-Qaeda extremists since May 2003, have warned that they will crack down on any attempt to undermine security during the hajj.")

        # Set up the CoreNLP persistence layer
        singleton = NLP_cache()
        cls.nlp_layer = singleton.nlp_layer

    def test_CheckIfGoverningVerbIsCorrect(self):
        # Easy case - direct dependency to taken
        info_a = self.nlp_layer.get_info_on_governing_verb("agency", 9, self.sentence)
        # info_a[0] contains the verb itself
        self.assertEqual(info_a[0], "taken")

        info_a = self.nlp_layer.get_info_on_governing_verb("space", 8, self.sentence)
        self.assertEqual(info_a[0], "taken")

        info_a = self.nlp_layer.get_info_on_governing_verb("we", 4, self.sentence)
        self.assertEqual(info_a[0], "learned")

        info_a = self.nlp_layer.get_info_on_governing_verb("giant", 14, self.sentence)
        self.assertEqual(info_a[0], "taken")

        info_a = self.nlp_layer.get_info_on_governing_verb("wave", 9, self.sentence2)
        self.assertEqual(info_a[0], "fighting")

        info_a = self.nlp_layer.get_info_on_governing_verb("suspected", 13, self.sentence2)
        self.assertEqual(info_a[0], "fighting")

        info_a = self.nlp_layer.get_info_on_governing_verb("Al-Qaeda", 14, self.sentence2)
        self.assertEqual(info_a[0], "fighting")

        info_a = self.nlp_layer.get_info_on_governing_verb("any", 28, self.sentence2)
        self.assertEqual(info_a[0], "crack")

    def test_CheckIfGoverningVerbMethodReturnsRightAux(self):
        info_a = self.nlp_layer.get_info_on_governing_verb("agency", 9, self.sentence)

        # info_a[1] contains the aux
        self.assertEqual(info_a[1], "has")

    def test_CheckIfGoverningVerbMethodReturnsRightPOS(self):
        info_a = self.nlp_layer.get_info_on_governing_verb("agency", 9, self.sentence)

        # info_a[2] contains the POS for the main verb and info_a[3] contains the POS for the aux
        self.assertEqual(info_a[2], "VBN")
        self.assertEqual(info_a[3], "VBZ")

    def test_CheckIfIsVerbMethodDetectsVerbs(self):
        info = self.nlp_layer.get_info_for_sentence(self.sentence)

        r = self.nlp_layer._is_verb("learned", info, 0)
        self.assertEqual(r, True)

        r = self.nlp_layer._is_verb("taken", info, 0)
        self.assertEqual(r, True)

        r = self.nlp_layer._is_verb("Finally", info, 0)
        self.assertEqual(r, False)

class TenseChoosing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the CoreNLP persistence layer
        singleton = NLP_cache()
        cls.nlp_layer = singleton.nlp_layer

    def test_IsPresentTenseRecognized(self):
        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He teaches math in school.", "teaches")
        self.assertEqual(Tense.PRESENT, tense)

        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He is teaching math in school.", "teaching")
        self.assertEqual(Tense.PRESENT, tense)

        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He has taught math in school.", "taught")
        self.assertEqual(Tense.PRESENT, tense)

        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He has been teaching math in school.", "teaching")
        self.assertEqual(Tense.PRESENT, tense)

        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He is taught math by his favorite teacher.", "taught")
        self.assertEqual(Tense.PRESENT, tense)

        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He is being taught math by his favorite teacher.", "taught")
        self.assertEqual(Tense.PRESENT, tense)

        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He has been taught math by his favorite teacher.", "taught")
        self.assertEqual(Tense.PRESENT, tense)

    def test_IsPastTenseRecognized(self):
        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He taught math in school.", "taught")
        self.assertEqual(Tense.PAST, tense)

        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He was teaching math in school.", "teaching")
        self.assertEqual(Tense.PAST, tense)

        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He had taught math in school.", "taught")
        self.assertEqual(Tense.PAST, tense)

        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He had been teaching math in school.", "teaching")
        self.assertEqual(Tense.PAST, tense)

        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He was taught math by his favorite teacher.", "taught")
        self.assertEqual(Tense.PAST, tense)

        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He was being taught math by his favorite teacher in school.", "taught")
        self.assertEqual(Tense.PAST, tense)

        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He had been taught math by his favorite teacher in school.", "taught")
        self.assertEqual(Tense.PAST, tense)

    def test_IsFutureTenseRecognized(self):
        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He will teach math in school.", "teach")
        self.assertEqual(Tense.FUTURE, tense)

        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He will be teaching math in school.", "teaching")
        self.assertEqual(Tense.FUTURE, tense)

        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He will have taught math in school.", "taught")
        self.assertEqual(Tense.FUTURE, tense)

        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He will have been teaching math in school.", "teaching")
        self.assertEqual(Tense.FUTURE, tense)

        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He will be taught by Mr. Peterson in school.", "taught")
        self.assertEqual(Tense.FUTURE, tense)

        tense_chooser = Tense_chooser(self.nlp_layer)
        tense = tense_chooser.get_tense_only_for_tests("He will have been taught by Mr. Peterson in school.", "taught")
        self.assertEqual(Tense.FUTURE, tense)

class TenseFeature(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        filename = "data/training/TBAQ-cleaned/TimeBank/ABC19980304.1830.1636.tml"
        filename_second = "data/training/TBAQ-cleaned/TimeBank/ABC19980304.1830.1636.tml"

        cls.text_obj = Text(filename)
        cls.text_obj_second = Text(filename_second)

        cls.entities = cls.text_obj.entities_order

        # Set up the CoreNLP persistence layer
        singleton = NLP_cache()
        cls.nlp_layer = singleton.nlp_layer

        cls.tense = Tense(cls.text_obj.relations[0], cls.nlp_layer)

    def test_ReturnTenseOfNounByLookingAtGoverningVerb(self):
        noun_event = self.entities[5]
        governing_verb_event = self.entities[4]

        governing_verb, index = self.nlp_layer.get_governing_verb(noun_event)

        potential_governing_verb_event = self.text_obj.try_to_find_governing_verb_as_event(governing_verb, index, noun_event)

        self.assertEqual(governing_verb_event, potential_governing_verb_event)

    def test_TenseWhenEventIsNotAVerb(self):
        # Find relation with event e52 with text "astronaut", which has no tense, as target
        rel_e52 = None
        for relation in self.text_obj_second.relations:
            if type(relation.target) == Event:
                if relation.target.eid == "e52":
                    rel_e52 = relation
                    break

        tense = Tense(relation, self.nlp_layer).target

        # Governing verb is "was picked" which is past
        self.assertEqual(tense, Tense.PAST)

class DependencyOrderFeature(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the CoreNLP persistence layer
        singleton = NLP_cache()
        cls.nlp_layer = singleton.nlp_layer

        filename = "data/training/TBAQ-cleaned/TimeBank/ABC19980304.1830.1636.tml"
        cls.text_obj = Text(filename)

        cls.relation = cls.text_obj.relations[0]
        cls.dependency_order = Dependency_order(cls.relation, cls.nlp_layer)

    def test_IsDependencyOrderCorrect(self):
        self.assertTrue(self.dependency_order._is_e1_governing_e2("been", "a"))
        self.assertTrue(self.dependency_order._is_e1_governing_e2("been", "has"))
        self.assertTrue(self.dependency_order._is_e1_governing_e2("charge", "mission"))
        self.assertFalse(self.dependency_order._is_e1_governing_e2("mission", "charge"))

class DurationFeature(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.duration_cache = Duration_cache()

    def test_IsRightDuration(self):
        # The "right" information are in event.lexicon.distributions
        self.assertEqual(self.duration_cache.word_likelihoods["crowd"], 3)
        self.assertEqual(self.duration_cache.word_likelihoods["accumulate"], 5)
        self.assertEqual(self.duration_cache.word_likelihoods["loom"], 7)
        self.assertEqual(self.duration_cache.word_likelihoods["forbid"], 1)

class Relations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename = "data/training/TBAQ-cleaned/TimeBank/ABC19980304.1830.1636.tml"
        cls.closure_test = "data/closure-test.tml"

    def test_AreThereMoreRelationsAfterProducingInversedRelations(self):
        text_obj = Text(self.filename, inverse=False, closure=False)
        parser_obj = Parser(self.filename, text_obj)

        before = len(parser_obj.relations)
        inversed = parser_obj.get_inversed_relations()
        after = len(parser_obj.relations + inversed)
        self.assertGreater(after, before)

    def test_AreThereMoreRelationsAfterProducingClosuredRelations(self):
        text_obj = Text(self.closure_test, inverse=False, closure=False)
        parser_obj = Parser(self.closure_test, text_obj)

        before = len(parser_obj.relations)
        closures = parser_obj.get_closured_relations()
        after = len(parser_obj.relations + closures)
        self.assertGreater(after, before)

    def test_CheckDistributionAfterInversedRelations(self):
        text_obj = Text(self.filename, inverse=True, closure=False)

        # Count temporal types
        BEFORE = AFTER = INCLUDES = IS_INCLUDED = ENDS = ENDED_BY = DURING = DURING_INV = IAFTER = IBEFORE = BEGINS = BEGUN_BY = 0
        for relation in text_obj.relations:
            if relation.relation_type == RelationType.BEFORE:
                BEFORE += 1
            elif relation.relation_type == RelationType.AFTER:
                AFTER += 1
            elif relation.relation_type == RelationType.INCLUDES:
                INCLUDES += 1
            elif relation.relation_type == RelationType.IS_INCLUDED:
                IS_INCLUDED += 1
            elif relation.relation_type == RelationType.ENDS:
                ENDS += 1
            elif relation.relation_type == RelationType.ENDED_BY:
                ENDED_BY += 1
            elif relation.relation_type == RelationType.DURING:
                DURING += 1
            elif relation.relation_type == RelationType.DURING_INV:
                DURING_INV += 1
            elif relation.relation_type == RelationType.IAFTER:
                IAFTER += 1
            elif relation.relation_type == RelationType.IBEFORE:
                IBEFORE += 1
            elif relation.relation_type == RelationType.BEGINS:
                BEGINS += 1
            elif relation.relation_type == RelationType.BEGUN_BY:
                BEGUN_BY += 1

        self.assertEqual(BEFORE, AFTER)
        self.assertEqual(INCLUDES, IS_INCLUDED)
        self.assertEqual(ENDS, ENDED_BY)
        self.assertEqual(DURING, DURING_INV)
        self.assertEqual(IAFTER, IBEFORE)
        self.assertEqual(BEGINS, BEGUN_BY)

    def test_AreThereTheRightClosures(self):
        text_obj = Text(self.closure_test, inverse=False, closure=False)
        parser_obj = Parser(self.closure_test, text_obj)

        e1 = parser_obj.events[0]
        e2 = parser_obj.events[1]
        e3 = parser_obj.events[2]
        e4 = parser_obj.events[3]
        # Existing relations: e1-e2, e2-e3, e3-e4

        r1 = Relation("closure", text_obj, e1, e3, RelationType.BEFORE)
        r2 = Relation("closure", text_obj, e2, e4, RelationType.BEFORE)
        # Only calculating transitives. Not transitives of transitives of ...
        # r3 = Relation("closure", text_obj, e1, e4, RelationType.BEFORE)

        closure_rel = parser_obj.get_closured_relations()

        self.assertIn(r1, closure_rel)
        self.assertIn(r2, closure_rel)
        # self.assertIn(r3, closure_rel)

    def test_AreThereTheRightClosuresAfterFullClosure(self):
        text_obj = Text(self.closure_test, inverse=False, closure=False)
        parser_obj = Parser(self.closure_test, text_obj, full_closure=True)

        e1 = parser_obj.events[0]
        e2 = parser_obj.events[1]
        e3 = parser_obj.events[2]
        e4 = parser_obj.events[3]
        # Existing relations: e1-e2, e2-e3, e3-e4

        r1 = Relation("closure", text_obj, e1, e3, RelationType.BEFORE)
        r2 = Relation("closure", text_obj, e2, e4, RelationType.BEFORE)
        r3 = Relation("closure", text_obj, e1, e4, RelationType.BEFORE)

        closure_rel = parser_obj.get_closured_relations()

        self.assertIn(r1, closure_rel)
        self.assertIn(r2, closure_rel)
        self.assertIn(r3, closure_rel)

    def test_IsThereTheRightAmountOfRelationsAfterClosures(self):
        text_obj = Text(self.closure_test, inverse=False, closure=False)
        parser_obj = Parser(self.closure_test, text_obj)

        closured_rel = parser_obj.get_closured_relations()

        self.assertEqual(len(closured_rel), 2)

class EntityExtraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        filename = "data/training/TBAQ-cleaned/TimeBank/ABC19980304.1830.1636.tml"
        cls.text_obj = Text(filename)

    def test_CheckForRightBeginAndEnd(self):
        entity = self.text_obj.text_structure.get_entities_ordered()[1]
        self.assertEqual(entity.begin, 8)
        self.assertEqual(entity.end, 13)

        entity = self.text_obj.text_structure.get_entities_ordered()[10]
        self.assertEqual(entity.begin, 16)
        self.assertEqual(entity.end, 28)

    def test_CheckForRightIndexOfEvents(self):
        learned = self.text_obj.text_structure.get_entities_ordered()[2]
        self.assertEqual(learned.index, 5)

        taken = self.text_obj.text_structure.get_entities_ordered()[3]
        self.assertEqual(taken.index, 12)

        boss = self.text_obj.text_structure.get_entities_ordered()[9]
        self.assertEqual(boss.index, 15)

class SystemRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class Testdata:
            def __init__(self):
                self.training = TrainingSet(False, "data/training/TBAQ-cleaned/TimeBank/ABC19980108.1830.0711.tml", "data/training/TBAQ-cleaned/TimeBank/AP900816-0139.tml", "data/training/TBAQ-cleaned/TimeBank/APW19980418.0210.tml")
                self.test = TestSet(False, "data/test/te3-platinum/AP_20130322.tml")
        cls.testdata = Testdata()

    def test_IsSystemRunningThroughWithAllFeatures(self):
        system = System(self.testdata)

        # Turn on features
        system.use_dependency_is_root()
        system.use_dependency_order()
        system.use_aspect()
        system.use_tense()
        system.use_same_tense()
        system.use_same_aspect()
        system.use_dependency_type()
        system.use_dct()
        system.use_type()
        system.use_same_polarity()
        system.use_polarity()
        system.use_class()
        system.use_entity_distance()
        system.use_textual_order()
        system.use_duration()
        system.use_duration_difference()
        system.use_same_pos()
        system.use_pos()
        system.use_temporal_signal()

        system.create_features()
        system.train()
        system.eval()
        self.assertTrue(True)

class ConstraintsComplete(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_SimpleGraph(self):
        text_obj = Text("data/simple-graph.tml", inverse=False, closure=False)

        A = text_obj.events[0]
        B = text_obj.events[1]
        C = text_obj.events[2]

        A_C_before = Relation("closure", text_obj, A, C, RelationType.BEFORE)

        result = [text_obj.relations[0], text_obj.relations[1], A_C_before]

        constraints = Constraints(text_obj, test=True)

        # A--before 0.9--B, B--before 0.9--C, A--after 0.7--C
        A_B = Directed_Pair(A, B, [0.9, 0, 0], [0, 1, 2])
        B_C = Directed_Pair(B, C, [0.9, 0, 0], [0, 1, 2])
        A_C = Directed_Pair(A, C, [0, 0, 0.7], [0, 1, 2])

        constraints.directed_pairs = [A_B, B_C, A_C]
        constraints._build_model()

        best_set = constraints.get_best_set()

        self.assertEqual(result, best_set)

    def test_SimpleGraph2(self):
        text_obj = Text("data/simple-graph.tml", inverse=False, closure=False)

        A = text_obj.events[0]
        B = text_obj.events[1]
        C = text_obj.events[2]

        # B-before-C will become B-after-C. Why? Becuase the relation has to exist due to the constraints and it doesn't make the graph invalid
        B_C_after = Relation("", text_obj, B, C, RelationType.AFTER)

        result = [text_obj.relations[0], B_C_after, text_obj.relations[2]]

        constraints = Constraints(text_obj, test=True)

        # A--before 0.9--B, B--before 0.6--C, A--after 0.7--C
        A_B = Directed_Pair(A, B, [0.9, 0, 0], [0, 1, 2])
        B_C = Directed_Pair(B, C, [0.6, 0, 0], [0, 1, 2])
        A_C = Directed_Pair(A, C, [0, 0, 0.7], [0, 1, 2])

        constraints.directed_pairs = [A_B, B_C, A_C]
        constraints._build_model()

        best_set = constraints.get_best_set()

        self.assertEqual(result, best_set)

    def test_AnotherSimpleGraph(self):
        text_obj = Text("data/simple-graph-2.tml", inverse=False, closure=False)

        A = text_obj.events[0]
        B = text_obj.events[1]
        C = text_obj.events[2]

        B_C_iafter = Relation("", text_obj, B, C, RelationType.IAFTER)

        result = [text_obj.relations[0], B_C_iafter, text_obj.relations[2]]

        constraints = Constraints(text_obj, test=True)

        # A--simultaneous 0.5--B, B--before 0.5--C, A--after 0.6--C
        A_B = Directed_Pair(A, B, [0, 0, 0, 0, 0, 0, 0, 0, 0.5], [0, 1, 2, 3, 4, 5, 6, 7, 8])
        B_C = Directed_Pair(B, C, [0.5, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 2, 3, 4, 5, 6, 7, 8])
        A_C = Directed_Pair(A, C, [0.1, 0, 0.6, 0, 0, 0, 0, 0, 0], [0, 1, 2, 3, 4, 5, 6, 7, 8])

        constraints.directed_pairs = [A_B, B_C, A_C]
        constraints._build_model()

        best_set = constraints.get_best_set()

        self.assertEqual(result, best_set)

    def test_AnotherSimpleGraph_2(self):
        text_obj = Text("data/simple-graph-2.tml", inverse=False, closure=False)

        A = text_obj.events[0]
        B = text_obj.events[1]
        C = text_obj.events[2]

        A_C_before = Relation("", text_obj, A, C, RelationType.BEFORE)

        result = [text_obj.relations[0], text_obj.relations[1], A_C_before]

        constraints = Constraints(text_obj, test=True)

        #                                           A--before 0.1--C
        # A--simultaneous 0.5--B, B--before 0.5--C, A--after 0.5--C
        A_B = Directed_Pair(A, B, [0, 0, 0, 0, 0, 0, 0, 0, 0.5], [0, 1, 2, 3, 4, 5, 6, 7, 8])
        B_C = Directed_Pair(B, C, [0.5, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 2, 3, 4, 5, 6, 7, 8])
        A_C = Directed_Pair(A, C, [0.1, 0, 0.5, 0, 0, 0, 0, 0, 0], [0, 1, 2, 3, 4, 5, 6, 7, 8])

        constraints.directed_pairs = [A_B, B_C, A_C]
        constraints._build_model()

        best_set = constraints.get_best_set()

        self.assertEqual(result, best_set)

class TransitivityConstraints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.constraints = Constraints(None, test=True)

    def test_CheckTargetEqualsSource(self):
        dummy_probabilities = [0.1, 0.2, 0.2, 0.3]
        dummy_classes = [0,1,2,3]
        # X before Y && Y before Z => X before Z
        pair1 = Directed_Pair("X", "Y", dummy_probabilities, dummy_classes)
        pair2 = Directed_Pair("Y", "Z", dummy_probabilities, dummy_classes)
        pair3 = Directed_Pair("X", "Z", dummy_probabilities, dummy_classes)
        v1 = Variable(None, pair1, RelationType.BEFORE)
        v2 = Variable(None, pair2, RelationType.BEFORE)
        v3 = Variable(None, pair3, RelationType.BEFORE)

        self.constraints.directed_pairs = [pair1, pair2, pair3]
        self.constraints.variables = [v1, v2, v3]

        triples = self.constraints._get_triples_by_rule(["A", RelationType.BEFORE, "B", "B", RelationType.BEFORE, "C", "A", RelationType.BEFORE, "C"])

        self.assertEqual([[v1, v2, v3]], triples)

    def test_CheckTargetEqualsSourceWithMore(self):
        dummy_probabilities = [0.1, 0.2, 0.2, 0.3]
        dummy_classes = [0,1,2,3]
        # X before Y && Y before Z => X before Z
        # X before Y && Y before D => X before D
        pair1 = Directed_Pair("X", "Y", dummy_probabilities, dummy_classes)
        pair2 = Directed_Pair("Y", "Z", dummy_probabilities, dummy_classes)
        pair3 = Directed_Pair("X", "Z", dummy_probabilities, dummy_classes)
        pair4 = Directed_Pair("Y", "D", dummy_probabilities, dummy_classes)
        pair5 = Directed_Pair("X", "D", dummy_probabilities, dummy_classes)
        v1 = Variable(None, pair1, RelationType.BEFORE)
        v2 = Variable(None, pair2, RelationType.BEFORE)
        v3 = Variable(None, pair3, RelationType.BEFORE)
        v4 = Variable(None, pair4, RelationType.BEFORE)
        v5 = Variable(None, pair5, RelationType.BEFORE)

        self.constraints.directed_pairs = [pair1, pair2, pair3, pair4, pair5]
        self.constraints.variables = [v1, v2, v3, v4, v5]

        triples = self.constraints._get_triples_by_rule(["A", RelationType.BEFORE, "B", "B", RelationType.BEFORE, "C", "A", RelationType.BEFORE, "C"])

        self.assertEqual([[v1, v2, v3], [v1, v4, v5]], triples)

    def test_CheckTargetEqualsSourceWithEvenMore(self):
        dummy_probabilities = [0.1, 0.2, 0.2, 0.3]
        dummy_classes = [0,1,2,3]
        # A before B && B before C && C before D => A before C, B before D, A before D
        pair1 = Directed_Pair("A", "B", dummy_probabilities, dummy_classes)
        pair2 = Directed_Pair("B", "C", dummy_probabilities, dummy_classes)
        pair3 = Directed_Pair("C", "D", dummy_probabilities, dummy_classes)
        pair4 = Directed_Pair("A", "C", dummy_probabilities, dummy_classes)
        pair5 = Directed_Pair("B", "D", dummy_probabilities, dummy_classes)
        pair6 = Directed_Pair("A", "D", dummy_probabilities, dummy_classes)
        v1 = Variable(None, pair1, RelationType.BEFORE)
        v2 = Variable(None, pair2, RelationType.BEFORE)
        v3 = Variable(None, pair3, RelationType.BEFORE)
        v4 = Variable(None, pair4, RelationType.BEFORE)
        v5 = Variable(None, pair5, RelationType.BEFORE)
        v6 = Variable(None, pair6, RelationType.BEFORE)

        self.constraints.directed_pairs = [pair1, pair2, pair3, pair4, pair5, pair6]
        self.constraints.variables = [v1, v2, v3, v4, v5, v6]

        triples = self.constraints._get_triples_by_rule(["A", RelationType.BEFORE, "B", "B", RelationType.BEFORE, "C", "A", RelationType.BEFORE, "C"])

        self.assertEqual(sorted([[v1, v5, v6], [v1, v2, v4], [v2, v3, v5], [v4, v3, v6]]), sorted(triples))

    def test_CheckSourcesAreEqual(self):
        dummy_probabilities = [0.1, 0.2, 0.2, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2]
        dummy_classes = [0,1,2,3,4,5,6,7,8]
        # A simultaneous B && A before C => B before C
        pair1 = Directed_Pair("A", "B", dummy_probabilities, dummy_classes)
        pair2 = Directed_Pair("A", "C", dummy_probabilities, dummy_classes)
        pair3 = Directed_Pair("B", "C", dummy_probabilities, dummy_classes)
        v1 = Variable(None, pair1, RelationType.SIMULTANEOUS)
        v2 = Variable(None, pair2, RelationType.BEFORE)
        v3 = Variable(None, pair3, RelationType.BEFORE)

        self.constraints.directed_pairs = [pair1, pair2, pair3]
        self.constraints.variables = [v1, v2, v3]

        triples = self.constraints._get_triples_by_rule(["A", RelationType.SIMULTANEOUS, "B", "A", RelationType.BEFORE, "C", "B", RelationType.BEFORE, "C"])

        self.assertEqual([[v1, v2, v3]], triples)

    def test_CheckTargetsEquals(self):
        dummy_probabilities = [0.1, 0.2, 0.2, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2]
        dummy_classes = [0,1,2,3,4,5,6,7,8]
        # A simultaneous B && C simultaneous B => A simultaneous C
        pair1 = Directed_Pair("A", "B", dummy_probabilities, dummy_classes)
        pair2 = Directed_Pair("C", "B", dummy_probabilities, dummy_classes)
        pair3 = Directed_Pair("A", "C", dummy_probabilities, dummy_classes)
        v1 = Variable(None, pair1, RelationType.SIMULTANEOUS)
        v2 = Variable(None, pair2, RelationType.SIMULTANEOUS)
        v3 = Variable(None, pair3, RelationType.SIMULTANEOUS)

        self.constraints.directed_pairs = [pair1, pair2, pair3]
        self.constraints.variables = [v1, v2, v3]

        triples = self.constraints._get_triples_by_rule(["A", RelationType.SIMULTANEOUS, "B", "C", RelationType.SIMULTANEOUS, "B", "A", RelationType.SIMULTANEOUS, "C"])

        self.assertEqual([[v1, v2, v3]], triples)

    def test_CheckSourceEqualsTarget(self):
        dummy_probabilities = [0.1, 0.2, 0.2, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2]
        dummy_classes = [0,1,2,3,4,5,6,7,8]
        # B simultaneous A && C simultaneous B => A simultaneous C
        pair1 = Directed_Pair("B", "A", dummy_probabilities, dummy_classes)
        pair2 = Directed_Pair("C", "B", dummy_probabilities, dummy_classes)
        pair3 = Directed_Pair("A", "C", dummy_probabilities, dummy_classes)
        v1 = Variable(None, pair1, RelationType.SIMULTANEOUS)
        v2 = Variable(None, pair2, RelationType.SIMULTANEOUS)
        v3 = Variable(None, pair3, RelationType.SIMULTANEOUS)

        self.constraints.directed_pairs = [pair1, pair2, pair3]
        self.constraints.variables = [v1, v2, v3]

        triples = self.constraints._get_triples_by_rule(["B", RelationType.SIMULTANEOUS, "A", "C", RelationType.SIMULTANEOUS, "B", "A", RelationType.SIMULTANEOUS, "C"])

        # TODO: Not sure if I really want this result
        self.assertEqual(sorted([[v1, v2, v3], [v2, v3, v1], [v3, v1, v2]]), sorted(triples))

    def test_CheckIfThereIsNoOutputIfThereIsNoGraph(self):
        dummy_probabilities = [0.1, 0.2, 0.2, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2]
        dummy_classes = [0,1,2,3,4,5,6,7,8]
        # A simultaneous B && C simultaneous B => A simultaneous C
        pair1 = Directed_Pair("A", "B", dummy_probabilities, dummy_classes)
        pair2 = Directed_Pair("C", "B", dummy_probabilities, dummy_classes)
        pair3 = Directed_Pair("A", "C", dummy_probabilities, dummy_classes)
        v1 = Variable(None, pair1, RelationType.BEFORE)
        v2 = Variable(None, pair2, RelationType.BEFORE)
        v3 = Variable(None, pair3, RelationType.AFTER)

        self.constraints.directed_pairs = [pair1, pair2, pair3]
        self.constraints.variables = [v1, v2, v3]

        triples = self.constraints._get_triples_by_rule(["A", RelationType.BEFORE, "B", "C", RelationType.BEFORE, "B", "A", RelationType.BEFORE, "C"])

        self.assertEqual([], triples)


if __name__ == '__main__':
    unittest.main()
