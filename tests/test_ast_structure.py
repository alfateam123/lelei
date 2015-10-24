import unittest
from lelei import parser as structureparser

class TestStructureParser(unittest.TestCase):
    def setUp(self):
        self.xmlSource = """
        <structure>
          <name>stdUDPHeader</name>
          <fields>
            <field type="uint16" bits="0">MessageID</field>
            <field type="uint16" bits="0">MessageLenght</field>
            <field type="uint32" bits="0">MessageCount</field>
            <field type="uint64" bits="0">MessageSendTime</field>
            <field type="uint32" bits="0">MessageChecksum</field>
          </fields>
        </structure>
        """
        self.parsed_doc = structureparser.parse(self.xmlSource)

    def test_nameIsCorrect(self):
        self.assertEqual(self.parsed_doc["name"], "stdUDPHeader")

    def test_numberOfFields(self):
        self.assertEqual(len(self.parsed_doc["fields"]), 5)

    def test_isLastFieldOk(self):
        self.assertEqual(self.parsed_doc["fields"][-1]["type"], "uint32")
        self.assertEqual(self.parsed_doc["fields"][-1]["bits"], 32)
        self.assertEqual(self.parsed_doc["fields"][-1]["name"], "MessageChecksum")

class TestStructureAutoSizing(unittest.TestCase):
    
    def test_bitsAreCalculatedCorrectly(self):
        self.assertEqual(structureparser.bitsForStructure("uint8",  3),  3)
        self.assertEqual(structureparser.bitsForStructure("uint8",  8),  8)
        self.assertEqual(structureparser.bitsForStructure("uint16", 0), 16)
        self.assertEqual(structureparser.bitsForStructure("uint32", 0), 32)

    def test_oversizedTypes(self):
        self.assertRaises(ValueError, lambda : structureparser.bitsForStructure("uint8", 13))
        self.assertRaises(ValueError, lambda : structureparser.bitsForStructure("uint16", 17))
        self.assertRaises(ValueError, lambda : structureparser.bitsForStructure("uint32", 33))
        self.assertRaises(ValueError, lambda : structureparser.bitsForStructure("uint64", 65))

    def test_negativesizedTypes(self):
        self.assertRaises(ValueError, lambda : structureparser.bitsForStructure("uint8", -1))
        self.assertRaises(ValueError, lambda : structureparser.bitsForStructure("uint16", -1))
        self.assertRaises(ValueError, lambda : structureparser.bitsForStructure("uint32", -1))
        self.assertRaises(ValueError, lambda : structureparser.bitsForStructure("uint64", -1))


    def test_fieldTypeIsNotDefined(self):
        self.assertRaises(ValueError, lambda : structureparser.bitsForStructure("float", 0))
        self.assertRaises(ValueError, lambda : structureparser.bitsForStructure("int", 0))
        self.assertRaises(ValueError, lambda : structureparser.bitsForStructure("uint", 0))
        self.assertRaises(ValueError, lambda : structureparser.bitsForStructure("uint3", 0))
        self.assertRaises(ValueError, lambda : structureparser.bitsForStructure("uint128", 0))
