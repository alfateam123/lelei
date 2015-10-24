import unittest
import xml.etree.ElementTree as ET
from lelei import builder as ws
from lelei import parser

#class TestBuilder(unittest.TestCase):
#    pass

class TestFieldBuilder(unittest.TestCase):

    def test_int8(self):
        parsed_doc = parser.parse_field(ET.fromstring('<field type="uint8">test</field>'))
        res = ws.build_field(parsed_doc)
        self.assertEqual("uint8 test;", res)

    def test_int8_nostmt(self):
        parsed_doc = parser.parse_field(ET.fromstring('<field type="uint8" nostmt="2">test</field>'))
        res = ws.build_field(parsed_doc)
        self.assertEqual("uint8{ns=0} test;", res)