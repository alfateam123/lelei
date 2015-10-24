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

def structure_name(doc):
    names = doc.findall("name")
    assert len(names) == 1
    return names[0].text

def parse_fields(doc):
    doc_fields = doc.findall("fields/field")
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
        field_ast["bits"] = bitsForStructure(field_doc.attrib["type"], 0)
    return field_ast

def build_ast(doc):
    ast = dict()
    ast["name"] = structure_name(doc)
    ast["fields"] = parse_fields(doc)
    return ast

def parse(str_):
    root = _getroot(str_)
    ast = build_ast(root)

    return ast