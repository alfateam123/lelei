import unittest
import xml.etree.ElementTree as ET
from lelei import parser as structureparser

class TestSpareType(unittest.TestCase):

    def test_spareField(self):
        spare_desc = ET.fromstring('<field type="spare" bits="8">woot</field>')
        parsed_field = structureparser.parse_field(spare_desc)
        self.assertEqual(parsed_field["name"], "woot")
        self.assertEqual(parsed_field["type"], "spare")
        self.assertEqual(parsed_field["bits"], 8)

    def test_emptySpareField(self):
        """
        You can't insert a 0-sized spare. It makes no sense, too.
        Just comment the field if you don't need a field anymore.
        """
        spare_desc = ET.fromstring('<field type="spare" bits="0">woot</field>')
        self.assertRaises(ValueError, lambda : structureparser.parse_field(spare_desc))

class TestFloat(unittest.TestCase):
    
    def test_float32(self):
        spare_desc = ET.fromstring('<field type="float32">woot</field>')
        parsed_field = structureparser.parse_field(spare_desc)
        self.assertEqual(parsed_field["name"], "woot")
        self.assertEqual(parsed_field["type"], "float32")
        self.assertEqual(parsed_field["bits"], 32)

    def test_float64(self):
        spare_desc = ET.fromstring('<field type="float64">woot</field>')
        parsed_field = structureparser.parse_field(spare_desc)
        self.assertEqual(parsed_field["name"], "woot")
        self.assertEqual(parsed_field["type"], "float64")
        self.assertEqual(parsed_field["bits"], 64)

class TestPaddingBits(unittest.TestCase):

    def test_paddingBits(self):
        padding_desc = ET.fromstring('<field type="padding">dis_not_pudding</field>')
        parsed_field = structureparser.parse_field(spare_desc)
        self.assertEqual(parsed_field["name"], "dis_not_pudding")
        self.assertEqual(parsed_field["type"], "padding")
        self.assertEqual(parsed_field["bits"], 0)

    def test_paddingBits(self):
        padding_desc = ET.fromstring('<field type="padding" bits="15">dis_not_pudding</field>')
        parsed_field = structureparser.parse_field(padding_desc)
        #`bits` is overridden
        self.assertEqual(parsed_field["bits"], 0) 