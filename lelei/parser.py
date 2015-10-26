import xml.etree.ElementTree as ET
import re
from .sizes import SIZE_CHECKERS

def _getroot(str_):
    return ET.fromstring(str_)

def bitsForStructure(struct_type, read_bits):
    try:
        return SIZE_CHECKERS[struct_type](read_bits)
    except KeyError:
        raise ValueError("the given structure type {} does not exist".format(struct_type))

def structure_name(doc, xpath_prefix="structure"):
    names = doc.findall("{prefix}/name".format(prefix=xpath_prefix))
    assert len(names) == 1, len(names)
    return names[0].text

def parse_fields(doc, xpath_prefix="structure"):
    doc_fields = doc.findall("{prefix}/fields/field".format(prefix=xpath_prefix))
    assert len(doc_fields) > 0
    fields = [parse_field(f_) for f_ in doc_fields]
    return fields

def parse_field(field_doc):
    field_ast = dict()
    field_ast["name"] = field_doc.text
    field_ast["type"] = field_doc.attrib["type"]
    #some fields (e.g. float32) have a fixed size, so it's useless
    # to set `bits=0` while defining such fields.
    try:
        #obviously, the KeyError is related to `bits` and not to `type`.
        field_ast["bits"] = bitsForStructure(field_doc.attrib["type"], int(field_doc.attrib["bits"]))
    except KeyError:
        try:
            field_ast["bits"] = bitsForStructure(field_doc.attrib["type"], 8*int(field_doc.attrib["lenght"]))
        except KeyError:
            try:
                field_ast["bits"] = bitsForStructure(field_doc.attrib["type"], 0)
            except ValueError as ve:
                if field_ast["type"] == "raw(*)":
                    field_ast["bits"] = 8
                else:
                    raise ve
    return field_ast

def struct_byteorder(doc):
    byteorder_xml = doc.findall("structure/byte_order")
    if len(byteorder_xml) >= 1:
        assert len(byteorder_xml) == 1, "`structure.byte_order` is defined too many times!"
        assert byteorder_xml[0].text in ["big_endian", "little_endian"]
        return byteorder_xml[0].text
    else:
        #default value
        return "big_endian"

def header_idfield(doc):
    idfield_xml = doc.findall("header/id_field_name")
    assert len(idfield_xml) == 1, "the `header.id_field_name` is not defined in the source file."
    return idfield_xml[0].text  

def protocol_info(doc):
    protocol_info = {"proto_name": None, "proto_short": None}
    try:
        protocol_info["proto_name"] = doc.findall("protocolname")[-1].text
    except IndexError:
        pass #TODO: should we raise an error there? we should, tho

    try:
        protocol_info["proto_short"] = doc.findall("protocolshort")[-1].text
    except IndexError:
        pass #TODO: raise an error there!

    return protocol_info


def struct_info(doc, xpath_prefix="structure"):
    struct_ast = dict()
    struct_ast["name"] = structure_name(doc, xpath_prefix)
    struct_ast["fields"] = parse_fields(doc, xpath_prefix)
    struct_ast["byte_order"] = struct_byteorder(doc)
    return struct_ast

def header_info(doc):
    header_info = struct_info(doc, "header")
    header_info["id_field_name"] = header_idfield(doc)
    return header_info

def build_ast(doc):
    ast = dict()
    ast["proto"]  = protocol_info(doc)
    ast["struct"] = struct_info(doc)
    ast["header"] = header_info(doc)
    return ast

def parse(str_):
    root = _getroot(str_)
    ast = build_ast(root)

    return ast
