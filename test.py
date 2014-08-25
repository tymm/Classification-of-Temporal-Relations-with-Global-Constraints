import unittest

from parsexml.text import Text
from Feature import Feature as Features
from parsexml.fakesentence import FakeSentence
from parsexml.sentence import Sentence
from lxml import etree
from helper.nlp_persistence import Nlp_persistence

class TextStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        filename = "data/training/TBAQ-cleaned/TimeBank/ABC19980304.1830.1636.tml"
        cls.text_obj = Text(filename)

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

        self.assertEqual(sentences[0], FakeSentence("19980304."))
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

        cls.text_obj = Text(filename)
        cls.text_obj_second = Text(filename_second)

        cls.sentences = [s for s in cls.text_obj.text_structure.get_structure()]
        cls.sentences_second = [s for s in cls.text_obj_second.text_structure.get_structure()]

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

class Feature(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        filename = "data/training/TBAQ-cleaned/TimeBank/ABC19980304.1830.1636.tml"
        text_obj = Text(filename)

        nlp_persistence_obj = Nlp_persistence()
        nlp_persistence_obj.load()

        cls.features = []

        for relation in text_obj.relations:
            f = Features(relation, None, None, nlp_persistence_obj)
            cls.features.append(f)

    def test_SentenceDistance(self):
        for feature in self.features:
            if feature.get_sentence_distance()[0] == None:
                print feature.relation.source
                print feature.relation.target
            self.assertNotEqual(feature.get_sentence_distance()[0], None)

class Sentences(unittest.TestCase):
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

        # Set up the CoreNLP persistence layer
        cls.nlp_layer = Nlp_persistence()
        cls.nlp_layer.load()

    def test_CheckIfGoverningVerbIsCorrect(self):
        # Easy case - direct dependency to taken
        info_a = self.sentence.get_info_on_governing_verb("agency", self.nlp_layer)
        # TODO: Add case which is harder: No direct dependency connection between non-verb and governing verb like with "space"

        # info_a[0] contains the verb itself
        self.assertEqual(info_a[0], "taken")

    def test_CheckIfGoverningVerbMethodReturnsRightAux(self):
        info_a = self.sentence.get_info_on_governing_verb("agency", self.nlp_layer)

        # info_a[1] contains the aux
        self.assertEqual(info_a[1], "has")

    def test_CheckIfGoverningVerbMethodReturnsRightPOS(self):
        info_a = self.sentence.get_info_on_governing_verb("agency", self.nlp_layer)

        # info_a[2] contains the POS for the main verb and info_a[3] contains the POS for the aux
        self.assertEqual(info_a[2], "VBN")
        self.assertEqual(info_a[3], "VBZ")

    def test_CheckIfIsVerbMethodDetectsVerbs(self):
        info = self.nlp_layer.get_info_for_sentence(self.sentence)

        r = self.sentence._is_verb("learned", info)
        self.assertEqual(r, True)

        r = self.sentence._is_verb("taken", info)
        self.assertEqual(r, True)

        r = self.sentence._is_verb("Finally", info)
        self.assertEqual(r, False)

if __name__ == '__main__':
    unittest.main()
