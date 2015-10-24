import xml.etree.ElementTree as ET
import re
from sizes import SIZE_CHECKERS

def _getroot(str_):
    return ET.fromstring(str_)	

def bitsForStructure(struct_type, read_bits):
    #works for int/uint32, etc.
    #bits_by_structType = int(re.findall("(\d+)$", struct_type)[-1])
    #assert bits_by_structType%8 == 0 and 0 < bits_by_structType <= 64, "{} is not a valid dimension for a type".format(bits_by_structType)
    #if read_bits > bits_by_structType:
    #    raise ValueError("you are asking for more bits than the type can contain! %s -> %d"%(struct_type, read_bits))
    
    #if read_bits == 0:
    #    return bits_by_structType
    #else:
    #    return read_bits
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
    field_ast["bits"] = bitsForStructure(field_doc.attrib["type"], int(field_doc.attrib["bits"]))
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