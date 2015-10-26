import unittest
import xml.etree.ElementTree as ET
from lelei import builder as ws
from lelei import parser

def norm_multiline_str(multiline_str):
	splitted_str = multiline_str.splitlines()
	if len(splitted_str[0]) == 0:
		splitted_str.pop(0)
	spaces = len(splitted_str[0]) - len(splitted_str[0].lstrip())
	return "\n".join(chunk[spaces:] for chunk in splitted_str if chunk[spaces:])

class TestFieldBuilder(unittest.TestCase):

    def test_int8(self):
        parsed_doc = parser.parse_field(ET.fromstring('<field type="uint8" bits="0">test</field>'))
        res = ws.build_field(parsed_doc)
        self.assertEqual("uint8 test;", res)

    @unittest.skip("no_statement has not been implemented yet, left for later")
    def test_int8_nostmt(self):
        parsed_doc = parser.parse_field(ET.fromstring('<field type="uint8"  bits="0" nostmt="2">test</field>'))
        res = ws.build_field(parsed_doc)
        self.assertEqual("uint8{ns=0} test;", res)

class TestStructBuilder(unittest.TestCase):

    def setUp(self):
    	self.xmlOneFieldSource = """
        <protocol>
    	<structure>
		  <name>stdUDPHeader</name>
		  <fields>
		    <field type="uint16" bits="0">MessageID</field>
		  </fields>
		</structure>
        </protocol>
		"""
    	self.xmlSource = """
        <protocol>
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

    def test_onefield_struct(self):
        parsed_doc = parser.parse(self.xmlOneFieldSource)
        res = ws.build_struct(parsed_doc["struct"])
        self.assertEqual(res, norm_multiline_str("""
        	struct stdUDPHeader
        	{
        	    uint16 MessageID;
        	}
        	""") )

    def test_multiplefields_struct(self):
        parsed_doc = parser.parse(self.xmlSource)
        res = ws.build_struct(parsed_doc["struct"])
        self.assertEqual(res, norm_multiline_str("""
        	struct stdUDPHeader
        	{
        	    uint16 MessageID;
        	    uint16 MessageLenght;
        	    uint32 MessageCount;
        	    uint64 MessageSendTime;
        	    uint32 MessageChecksum;
        	}
        	""") )
