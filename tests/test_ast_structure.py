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

    def test_struct_byteorder_default(self):
        parsed_doc = ET.fromstring("<protocol><structure></structure></protocol>")
        self.assertEqual(structureparser.struct_byteorder(parsed_doc), "big_endian")

    def test_struct_byteorder_found_bigendian(self):
        parsed_doc = ET.fromstring("<protocol><structure><byte_order>big_endian</byte_order></structure></protocol>")
        self.assertEqual(structureparser.struct_byteorder(parsed_doc), "big_endian")

    def test_struct_byteorder_found_littleendian(self):
        parsed_doc = ET.fromstring("<protocol><structure><byte_order>little_endian</byte_order></structure></protocol>")
        self.assertEqual(structureparser.struct_byteorder(parsed_doc), "little_endian")

    def test_struct_byteorder_found_as_host(self):
        parsed_doc = ET.fromstring("<protocol><structure><byte_order>as_host</byte_order></structure></protocol>")
        self.assertEqual(structureparser.struct_byteorder(parsed_doc), "as_host")

    def test_struct_byteorder_found_error(self):
        parsed_doc = ET.fromstring("<protocol><structure><byte_order>error_endian</byte_order></structure></protocol>")
        self.assertRaises(ValueError, lambda : structureparser.struct_byteorder(parsed_doc))

    def test_struct_field_repeated_default(self):
        #no one has a `repeated` attribute, so it's ok for a "default :D"
        self.assertEqual(self.parsed_doc["struct"]["fields"][0]["repeated"], 1)

    def test_struct_field_repeated(self):
        xml_doc = ET.fromstring("""<field repeated="5" type="uint8">spare</field>""")
        self.assertEqual(structureparser.struct_field_repeated(xml_doc), 5)

    def test_struct_field_repeated_zero(self):
        xml_doc = ET.fromstring("""<field repeated="0" type="uint8">spare</field>""")
        self.assertRaises(ValueError, lambda : structureparser.struct_field_repeated(xml_doc))

    def test_struct_field_repeated_negative(self):
        xml_doc = ET.fromstring("""<field repeated="-15" type="uint8">spare</field>""")
        self.assertRaises(ValueError, lambda : structureparser.struct_field_repeated(xml_doc))

    def test_struct_field_repeated_useavariable(self):
        xml_doc = ET.fromstring("""<field repeated="number_of_numbers" type="uint8">spare</field>""")
        self.assertEqual(structureparser.struct_field_repeated(xml_doc), "number_of_numbers")

class TestProtocolInfo(unittest.TestCase):

    def setUp(self):
        with open("tests/test_data/stdUDPHeader.xml") as test_data:
            self.xmlSource = test_data.read()
        self.parsed_doc = structureparser.parse(self.xmlSource)

    def test_protoinfo(self):
        self.assertEqual(self.parsed_doc["proto"]["proto_name"],  "Lelei Protocol")
        self.assertEqual(self.parsed_doc["proto"]["proto_short"], "lelei")

    def test_protoshort_notfound(self):
        xml_doc = ET.fromstring("<protocol><protocolname>proto_name</protocolname></protocol>")
        parsed_doc = structureparser.protocol_info(xml_doc)
        self.assertEqual(parsed_doc["proto_name"], "proto_name")
        self.assertEqual(parsed_doc["proto_short"], "proto_name")

    def test_protoshort_notfound_spaces(self):
        xml_doc = ET.fromstring("<protocol><protocolname>proto name</protocolname></protocol>")
        parsed_doc = structureparser.protocol_info(xml_doc)
        self.assertEqual(parsed_doc["proto_name"], "proto name")
        self.assertEqual(parsed_doc["proto_short"], "pn")

    def test_protoname_notfount(self):
        xml_doc = ET.fromstring("<protocol><protocolshort>prott</protocolshort></protocol>")
        self.assertRaises(ValueError, lambda : structureparser.protocol_info(xml_doc))


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

    def test_header_notfound(self):
        parsed_doc = ET.fromstring("<protocol><structure><byte_order>error_endian</byte_order></structure></protocol>")
        self.assertRaises(AssertionError, lambda : structureparser.header_idfield(parsed_doc))

