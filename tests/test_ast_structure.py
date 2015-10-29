import unittest
import xml.etree.ElementTree as ET
from lelei import parser as structureparser

class TestASTChecker(unittest.TestCase):
    """
    this testcase checks for things that are common
    to _every_ correctly parsed document: the AST.
    """

    def setUp(self):
        with open("tests/test_data/stdUDPHeader.xml") as test_data:
            self.xmlSource = test_data.read()
        self.parsed_doc = structureparser.parse(self.xmlSource)

    def test_ast_has_proto(self):
        self.assertTrue(self.parsed_doc.get("proto", False))
        self.assertTrue(self.parsed_doc["proto"].get("proto_name", False))
        self.assertTrue(self.parsed_doc["proto"].get("proto_short", False))

    def test_ast_has_struct(self):
        self.assertTrue(self.parsed_doc.get("structures", False))
        self.assertTrue(self.parsed_doc["structures"][0].get("name", False))
        #py3k removes dict.has_key. guido, come on...
        #the first version was self.parsed_doc["struct"].get("fields", False)
        #but... what if you have an empty structure? to be sure,
        # we just check that the "fields" key is present.
        self.assertTrue("fields" in self.parsed_doc["structures"][0].keys())

    def test_ast_has_header(self):
        self.assertTrue(self.parsed_doc.get("header", False))
        self.assertTrue(self.parsed_doc["header"].get("id_field_name", False))

    def test_ast_has_enums(self):
        #no enum is legit, so we just check the field is there,
        # not its truthness
        self.assertTrue("enums" in self.parsed_doc.keys())

class TestStructParser(unittest.TestCase):

    def setUp(self):
        with open("tests/test_data/stdUDPHeader.xml") as test_data:
            self.xmlSource = test_data.read()
        self.parsed_doc = structureparser.parse(self.xmlSource)

    def test_numberOfStructures(self):
        self.assertEqual(len(self.parsed_doc["structures"]), 2)

    def test_nameIsCorrect(self):
        self.assertEqual(self.parsed_doc["structures"][0]["name"], "stdUDPHeader")

    def test_struct_id_isCorrect(self):
        self.assertEqual(self.parsed_doc["structures"][0]["struct_id"], 10100)
        self.assertEqual(self.parsed_doc["structures"][1]["struct_id"], 10200)

    def test_numberOfFields(self):
        self.assertEqual(len(self.parsed_doc["structures"][0]["fields"]), 5)

    def test_isLastFieldOk(self):
        self.assertEqual(self.parsed_doc["structures"][0]["fields"][-1]["type"], "uint32")
        self.assertEqual(self.parsed_doc["structures"][0]["fields"][-1]["bits"], 32)
        self.assertEqual(self.parsed_doc["structures"][0]["fields"][-1]["name"], "MessageChecksum")

    def test_struct_byteorder_default(self):
        parsed_doc = ET.fromstring("<structure></structure>")
        self.assertEqual(structureparser.struct_byteorder(parsed_doc), "big_endian")

    def test_struct_byteorder_found_bigendian(self):
        parsed_doc = ET.fromstring("<structure><byte_order>big_endian</byte_order></structure>")
        self.assertEqual(structureparser.struct_byteorder(parsed_doc), "big_endian")

    def test_struct_byteorder_found_littleendian(self):
        parsed_doc = ET.fromstring("<structure><byte_order>little_endian</byte_order></structure>")
        self.assertEqual(structureparser.struct_byteorder(parsed_doc), "little_endian")

    def test_struct_byteorder_found_as_host(self):
        parsed_doc = ET.fromstring("<structure><byte_order>as_host</byte_order></structure>")
        self.assertEqual(structureparser.struct_byteorder(parsed_doc), "as_host")

    def test_struct_byteorder_found_error(self):
        parsed_doc = ET.fromstring("<structure><byte_order>error_endian</byte_order></structure>")
        self.assertRaises(ValueError, lambda : structureparser.struct_byteorder(parsed_doc))

    def test_struct_field_repeated_default(self):
        xml_doc = ET.fromstring("""<field type="uint8">spare</field>""")
        self.assertEqual(structureparser.struct_field_repeated(xml_doc), 1)

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

class TestEnums(unittest.TestCase):
    def setUp(self):
        self.xmlSingleEnum = """
        <protocol><enums><enum>
          <name>messageid_enum</name>
          <values>
            <value id="100">Not_Enough</value>
            <value id="200">Some</value>
            <value id="300">Warmongers</value>
          </values>
        </enum></enums></protocol>
        """

        self.xmlMultipleEnums = """
        <protocol><enums>
          <enum>
            <name>messageid_enum_multi</name>
            <values><value id="100">Maybe_is_Enough</value></values>
          </enum>
          <enum>
            <name>messageid_enum_2</name>
            <values><value id="0x200">woot</value></values>
          </enum>
        </enums></protocol>
        """

        self.noEnums = "<protocol><enums></enums></protocol>"

    def test_noEnums(self):
        xml_doc = ET.fromstring(self.noEnums)
        parsed_doc = structureparser.global_enums(xml_doc)
        self.assertEqual(len(parsed_doc), 0)

    def test_singleEnum(self):
        xml_doc = ET.fromstring(self.xmlSingleEnum)
        parsed_doc = structureparser.global_enums(xml_doc)
        self.assertEqual(len(parsed_doc), 1)
        self.assertEqual(parsed_doc[0]["name"], "messageid_enum")

    def test_singleEnum_areEnumsReadCorrectly(self):
        xml_doc = ET.fromstring(self.xmlSingleEnum)
        enum_ast = structureparser.global_enums(xml_doc)[0]["values"][-1]
        self.assertEqual(enum_ast["id"], 300)
        self.assertEqual(enum_ast["name"], "Warmongers")

    def test_multipleEnums(self):
        xml_doc = ET.fromstring(self.xmlMultipleEnums)
        parsed_doc = structureparser.global_enums(xml_doc)
        self.assertEqual(len(parsed_doc), 2)
        self.assertEqual(parsed_doc[0]["name"], "messageid_enum_multi")
        self.assertEqual(parsed_doc[1]["name"], "messageid_enum_2")

    def test_multipleEnums_areEnumsReadCorrectly(self):
        xml_doc = ET.fromstring(self.xmlMultipleEnums)
        parsed_doc = structureparser.global_enums(xml_doc)
        self.assertEqual(parsed_doc[0]["values"][0]["name"], "Maybe_is_Enough")
        self.assertEqual(parsed_doc[1]["values"][0]["id"], 0x200)

class TestSingleEnum(unittest.TestCase):

    #TODO: what if we get an enum with no fields?

    def setUp(self):
        self.xmlWrongID = """<value id="asdf">woot_woot</value>""" 
        self.xmlHexaID = """<value id="0x300">w00t</value>"""
        self.xmlSingleEnum = """
        <enum>
          <size>8</size>
          <name>messageid_enum</name>
          <values>
            <value id="100">Not_Enough</value>
            <value id="200">Some</value>
            <value id="300">Warmongers</value>
          </values>
        </enum>
        """
        self.xmlDefaultSize = """
        <enum>
          <name>messageid_enum</name>
          <values>
            <value id="500">Not_Found</value>
          </values>
        </enum>
        """
        self.xmlErroneousSize_toobig = """
        <enum>
          <size>64</size>
          <name>messageid_enum</name>
          <values>
            <value id="500">Not_Found</value>
          </values>
        </enum>
        """
        self.xmlErroneousSize_toolow = """
        <enum>
          <size>-1</size>
          <name>messageid_enum</name>
          <values>
            <value id="500">Not_Found</value>
          </values>
        </enum>
        """
        self.xmlErroneousSize_zero = """
        <enum>
          <size>0</size>
          <name>messageid_enum</name>
          <values>
            <value id="500">Not_Found</value>
          </values>
        </enum>
        """


    def test_enum_nameIsReadCorrectly(self):
        xml_doc = ET.fromstring(self.xmlSingleEnum)
        ast = structureparser.parse_enum(xml_doc)
        self.assertEqual(ast["name"], "messageid_enum")

    def test_enum_valuesReadCorrectly(self):
        xml_doc = ET.fromstring(self.xmlSingleEnum)
        ast = structureparser.parse_enum(xml_doc)
        self.assertEqual(len(ast["values"]), 3)
        self.assertEqual(ast["values"][-1]["id"], 300)
        self.assertEqual(ast["values"][0]["name"], "Not_Enough")

    def test_enum_wrongID(self):
        xml_doc = ET.fromstring(self.xmlWrongID)
        self.assertRaises(ValueError, lambda : structureparser.parse_enum_pair(xml_doc))

    def test_enum_hexaID(self):
        xml_doc = ET.fromstring(self.xmlHexaID)
        ast = structureparser.parse_enum_pair(xml_doc)
        self.assertEqual(ast["id"], 0x300)

    def test_enum_size(self):
        xml_doc = ET.fromstring(self.xmlSingleEnum)
        ast = structureparser.parse_enum(xml_doc)
        self.assertEqual(ast["size"], 8)

    def test_enum_size_default(self):
        xml_doc = ET.fromstring(self.xmlDefaultSize)
        ast = structureparser.parse_enum(xml_doc)
        self.assertEqual(ast["size"], 32)

    def test_enum_size_tooBig(self):
        xml_doc = ET.fromstring(self.xmlErroneousSize_toobig)
        self.assertRaises(AssertionError, lambda : structureparser.parse_enum(xml_doc))

    def test_enum_size_tooLow(self):
        xml_doc = ET.fromstring(self.xmlErroneousSize_toolow)
        self.assertRaises(AssertionError, lambda : structureparser.parse_enum(xml_doc))

    def test_enum_size_zero(self):
        xml_doc = ET.fromstring(self.xmlErroneousSize_zero)
        self.assertRaises(AssertionError, lambda : structureparser.parse_enum(xml_doc))

