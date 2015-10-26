import unittest
import xml.etree.ElementTree as ET
from lelei import parser as structureparser

class TestStructureParser(unittest.TestCase):
    def setUp(self):
        self.xmlSource = """
        <protocol>
          <protocolname>Lelei Protocol</protocolname>
          <protocolshort>lelei</protocolshort>
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
        </protocol>
        """
        self.parsed_doc = structureparser.parse(self.xmlSource)

    def test_nameIsCorrect(self):
        self.assertEqual(self.parsed_doc["struct"]["name"], "stdUDPHeader")

    def test_numberOfFields(self):
        self.assertEqual(len(self.parsed_doc["struct"]["fields"]), 5)

    def test_isLastFieldOk(self):
        self.assertEqual(self.parsed_doc["struct"]["fields"][-1]["type"], "uint32")
        self.assertEqual(self.parsed_doc["struct"]["fields"][-1]["bits"], 32)
        self.assertEqual(self.parsed_doc["struct"]["fields"][-1]["name"], "MessageChecksum")


    def test_protoinfo(self):
        self.assertEqual(self.parsed_doc["proto"]["proto_name"],   "Lelei Protocol")
        self.assertEqual(self.parsed_doc["proto"]["proto_short"], "lelei")
