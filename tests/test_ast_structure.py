import unittest
import xml.etree.ElementTree as ET
from lelei import parser as structureparser

class TestStructParser(unittest.TestCase):

    def setUp(self):
        with open("tests/test_data/stdUDPHeader.xml") as test_data:
            self.xmlSource = test_data.read()
        self.parsed_doc = structureparser.parse(self.xmlSource)

    def test_nameIsCorrect(self):
        self.assertEqual(self.parsed_doc["struct"]["name"], "stdUDPHeader")

    def test_numberOfFields(self):
        self.assertEqual(len(self.parsed_doc["struct"]["fields"]), 5)

    def test_isLastFieldOk(self):
        self.assertEqual(self.parsed_doc["struct"]["fields"][-1]["type"], "uint32")
        self.assertEqual(self.parsed_doc["struct"]["fields"][-1]["bits"], 32)
        self.assertEqual(self.parsed_doc["struct"]["fields"][-1]["name"], "MessageChecksum")

class TestProtocolInfo(unittest.TestCase):

    def setUp(self):
        with open("tests/test_data/stdUDPHeader.xml") as test_data:
            self.xmlSource = test_data.read()
        self.parsed_doc = structureparser.parse(self.xmlSource)

    def test_protoinfo(self):
        self.assertEqual(self.parsed_doc["proto"]["proto_name"],   "Lelei Protocol")
        self.assertEqual(self.parsed_doc["proto"]["proto_short"], "lelei")

class TestHeaderInfo(unittest.TestCase):

    def setUp(self):
        with open("tests/test_data/stdUDPHeader.xml") as test_data:
            self.xmlSource = test_data.read()
        self.parsed_doc = structureparser.parse(self.xmlSource)

    def test_header_isdefined(self):
        self.assertTrue(self.parsed_doc.get("header", False))

    def test_header_name(self):
        self.assertEqual(self.parsed_doc["header"]["name"], "muhheader")

    def test_header_has_id_field_name(self):
        self.assertTrue(self.parsed_doc["header"].get("id_field_name", False))
        self.assertEqual(self.parsed_doc["header"]["id_field_name"], "PacketID")