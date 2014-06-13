import unittest

from Parser import Parser
from Feature import Feature as Features

class TextStructure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        filename = "data/training/TBAQ-cleaned/TimeBank/ABC19980304.1830.1636.tml"
        parser_obj = Parser(filename)
        cls.text_obj = parser_obj.get_text_object()

    def test_RightOrderOfEntities(self):
        entities_ordered = self.text_obj.text_structure.get_entities_ordered()

        self.assertEqual(entities_ordered[0].tid, "t32")
        self.assertEqual(entities_ordered[1].eid, "e1")
        self.assertEqual(entities_ordered[2].eid, "e2")
        self.assertEqual(entities_ordered[3].eid, "e3")
        self.assertEqual(entities_ordered[4].eid, "e37")
        self.assertEqual(entities_ordered[5].eid, "e38")
        self.assertEqual(entities_ordered[6].tid, "t33")
        self.assertEqual(entities_ordered[7].eid, "e40")
        self.assertEqual(entities_ordered[8].eid, "e41")
        self.assertEqual(entities_ordered[9].tid, "t34")
        self.assertEqual(entities_ordered[10].eid, "e6")
        self.assertEqual(entities_ordered[11].eid, "e7")
        self.assertEqual(entities_ordered[12].eid, "e254")
        self.assertEqual(entities_ordered[13].tid, "t55")
        self.assertEqual(entities_ordered[14].eid, "e68")
        self.assertEqual(entities_ordered[15].eid, "e44")
        self.assertEqual(entities_ordered[16].eid, "e10")
        self.assertEqual(entities_ordered[17].eid, "e20")
        self.assertEqual(entities_ordered[18].tid, "t36")
        self.assertEqual(entities_ordered[19].eid, "e51")
        self.assertEqual(entities_ordered[20].eid, "e22")
        self.assertEqual(entities_ordered[21].eid, "e52")
        self.assertEqual(entities_ordered[22].eid, "e23")
        self.assertEqual(entities_ordered[23].eid, "e24")
        self.assertEqual(entities_ordered[24].eid, "e25")
        self.assertEqual(entities_ordered[25].eid, "e26")
        self.assertEqual(entities_ordered[26].eid, "e27")
        self.assertEqual(entities_ordered[27].eid, "e28")
        self.assertEqual(entities_ordered[28].eid, "e30")

class Feature(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        filename = "data/training/TBAQ-cleaned/TimeBank/ABC19980304.1830.1636.tml"
        parser_obj = Parser(filename)
        text_obj = parser_obj.get_text_object()

        cls.features = []

        for relation in text_obj.relations:
            f = Features(relation)
            cls.features.append(f)

    def test_SentenceDistance(self):
        for feature in self.features:
            if feature.get_sentence_distance()[0] == None:
                print feature.relation.source
                print feature.relation.target
            self.assertNotEqual(feature.get_sentence_distance()[0], None)


if __name__ == '__main__':
    unittest.main()
