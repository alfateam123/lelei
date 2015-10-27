import unittest
import xml.etree.ElementTree as ET
from lelei import builder as ws
from lelei import parser
import re

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

    def test_int8_repeated_onetime(self):
        parsed_doc = parser.parse_field(ET.fromstring('<field type="uint8" repeated="1">test</field>'))
        res = ws.build_field(parsed_doc)
        self.assertEqual("uint8 test;", res)

    def test_int8_repeated(self):
        parsed_doc = parser.parse_field(ET.fromstring('<field type="uint8" repeated="5">test</field>'))
        res = ws.build_field(parsed_doc)
        self.assertEqual("uint8[5] test;", res)

    # @unittest.skip("no_statement has not been implemented yet, left for later")
    # def test_int8_nostmt(self):
    #     parsed_doc = parser.parse_field(ET.fromstring('<field type="uint8"  bits="0" nostmt="2">test</field>'))
    #     res = ws.build_field(parsed_doc)
    #     self.assertEqual("uint8{ns=0} test;", res)

class TestStructBuilder(unittest.TestCase):

    def setUp(self):
        with open("tests/test_data/onefield.xml") as onefield:
            self.xmlOneFieldSource = onefield.read()

        with open("tests/test_data/stdUDPHeader.xml") as stdUDPHeader:
            self.xmlSource = stdUDPHeader.read()

    def test_onefield_struct(self):
        parsed_doc = parser.parse(self.xmlOneFieldSource)
        res = ws.build_struct(parsed_doc["struct"], parsed_doc["header"]["name"])
        self.assertEqual(res, norm_multiline_str("""
            struct stdUDPHeader
            {
                byte_order big_endian;
                muhheader header;
                uint16 MessageID;
            }
            """) )

    def test_multiplefields_struct(self):
        parsed_doc = parser.parse(self.xmlSource)
        res = ws.build_struct(parsed_doc["struct"], parsed_doc["header"]["name"])
        self.assertEqual(res, norm_multiline_str("""
            struct stdUDPHeader
            {
                byte_order big_endian;
                muhheader header;
                uint16 MessageID;
                uint16 MessageLenght;
                uint32 MessageCount;
                uint64 MessageSendTime;
                uint32 MessageChecksum;
            }
            """) )

class TestWSGDNames(unittest.TestCase):

    def setUp(self):
        with open("tests/test_data/stdUDPHeader.xml") as stdUDPHeader:
            self.xmlSource = stdUDPHeader.read()
        parsed_doc = parser.parse(self.xmlSource)
        self.res = ws.build_wsgd(parsed_doc, "stdUDPHeader")

    def _find_keyword(self, keyword, built):
        return [line for line in built.splitlines() if line.startswith(keyword.upper())][0]

    def _get_values(self, keyword_line):
        return re.findall("^[A-Z_a-z]+[ \t]+(.+)", keyword_line)

    def _get_value(self, keyword_line):
        return self._get_values(keyword_line)[0]

    def test_printed_protoname_isnotempty(self):
        protoname = self._find_keyword("PROTONAME", self.res).strip()
        self.assertNotEqual(protoname, "PROTONAME")
        self.assertEqual(self._get_value(protoname), "Lelei Protocol")

    def test_printed_protoshortname_isnotempty(self):
        protoshortname = self._find_keyword("PROTOSHORTNAME", self.res).strip()
        self.assertNotEqual(protoshortname, "PROTOSHORTNAME")
        self.assertEqual(self._get_value(protoshortname), "lelei")

    def test_printed_protoabbrev_isnotempty(self):
        protoabbrev = self._find_keyword("PROTOABBREV", self.res).strip()
        self.assertNotEqual(protoabbrev, "PROTOABBREV")
        self.assertEqual(self._get_value(protoabbrev), "lelei")

    def test_printed_header_type(self):
        headertype = self._find_keyword("MSG_HEADER_TYPE", self.res).strip()
        self.assertNotEqual(headertype, "MSG_HEADER_TYPE")
        self.assertEqual(self._get_value(headertype), "muhheader")

    def test_printed_idfield(self):
        headerid = self._find_keyword("MSG_ID_FIELD_NAME", self.res).strip()
        self.assertNotEqual(headerid, "MSG_ID_FIELD_NAME")
        self.assertEqual(self._get_value(headerid), "PacketID")
