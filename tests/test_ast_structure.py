import unittest
from lelei import parser as structureparser
import xml.sax

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

    def test_isReadCorrectly(self):
        xml.sax.parseString(self.xmlSource, structureparser.StructureParser())

    def test_nameIsCorrect(self):
        parser = structureparser.StructureParser()
        xml.sax.parseString(self.xmlSource, parser)
        self.assertEqual(parser._ast["name"], "stdUDPHeader")

    def test_numberOfFields(self):
        parser = structureparser.StructureParser()
        xml.sax.parseString(self.xmlSource, parser)
        self.assertEqual(len(parser._ast["fields"]), 5)

    def test_bitsAreCalculatedCorrectly(self):
        parser = structureparser.StructureParser()
        self.assertEqual(parser.bitsForStructure("uint8",  3),  3)
        self.assertEqual(parser.bitsForStructure("uint8",  8),  8)
        self.assertEqual(parser.bitsForStructure("uint16", 0), 16)
        self.assertEqual(parser.bitsForStructure("uint32", 0), 32)
        self.assertRaises(ValueError, lambda : parser.bitsForStructure("uint8", 13))

    def test_fieldTypeIsNotDefined(self):
        parser = structureparser.StructureParser()
        self.assertRaises(IndexError, lambda : parser.bitsForStructure("float", 0))
        self.assertRaises(IndexError, lambda : parser.bitsForStructure("int", 0))
        self.assertRaises(IndexError, lambda : parser.bitsForStructure("uint", 0))
        self.assertRaises(AssertionError, lambda : parser.bitsForStructure("uint3", 0))
        #self.assertRaises(AssertionError, lambda : parser.bitsForStructure("uint24", 0))
        self.assertRaises(AssertionError, lambda : parser.bitsForStructure("uint128", 0))


    def test_isLastFieldOk(self):
        parser = structureparser.StructureParser()
        xml.sax.parseString(self.xmlSource, parser)
        self.assertEqual(parser._ast["fields"][-1]["type"], "uint32")
        self.assertEqual(parser._ast["fields"][-1]["bits"], 32)
        self.assertEqual(parser._ast["fields"][-1]["name"], "MessageChecksum")


if __name__ == "__main__":
    unittest.main()
