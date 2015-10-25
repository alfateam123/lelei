import unittest
import xml.etree.ElementTree as ET
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

class TestFieldParsing(unittest.TestCase):

    def test_nostatement_isnotset(self):
        spare_desc = ET.fromstring('<field type="spare" bits="8">woot</field>')
        parsed_field = structureparser.parse_field(spare_desc)
        self.assertEqual(parsed_field["no_statement"], None)

    def test_nostatement_isset(self):
        spare_desc = ET.fromstring('<field type="spare" bits="8" nostmt="2">woot</field>')
        parsed_field = structureparser.parse_field(spare_desc)
        self.assertEqual(parsed_field["no_statement"], "2")
