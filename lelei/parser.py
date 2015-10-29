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
    assert len(names) == 1, len(names)
    return names[0].text

def structure_id(doc):
    ids = doc.findall("struct_id")
    assert len(ids) == 1, len(ids)
    return int(ids[0].text)

def parse_fields(doc):
    doc_fields = doc.findall("fields/field")
    assert len(doc_fields) > 0
    fields = [parse_field(f_) for f_ in doc_fields]
    return fields

def struct_field_lenght(field_doc, field_ast):
    lenght_ast = dict()
    #some fields (e.g. float32) have a fixed size, so it's useless
    # to set `bits=0` while defining such fields.
    try:
        #obviously, the KeyError is related to `bits` and not to `type`.
        lenght_ast["bits"] = bitsForStructure(field_doc.attrib["type"], int(field_doc.attrib["bits"]))
    except KeyError:
        try:
            lenght_ast["bits"] = bitsForStructure(field_doc.attrib["type"], 8*int(field_doc.attrib["lenght"]))
        except KeyError:
            try:
                lenght_ast["bits"] = bitsForStructure(field_doc.attrib["type"], 0)
            except ValueError as ve:
                if field_ast["type"] == "raw(*)":
                    lenght_ast["bits"] = 8
                else:
                    raise ve
    return lenght_ast

def struct_field_repeated(field_doc):
    #try to read it from the attributes. if it's not there, return a default
    try:
        rep_value = field_doc.attrib["repeated"]
    except KeyError:
        return 1

    #try to check if it's an integer. if it's not, return it
    try:
        rep_value = int(rep_value)
    except ValueError:
        return rep_value

    if rep_value <= 0:
        raise ValueError("the given `field.repeated` value ({0}) is not a natural number!".format(rep_value))
    return rep_value

def parse_field(field_doc):
    field_ast = dict()
    field_ast["name"] = field_doc.text
    field_ast["type"] = field_doc.attrib["type"]
    field_ast["bits"] = struct_field_lenght(field_doc, field_ast)["bits"]
    field_ast["repeated"] = struct_field_repeated(field_doc)
    return field_ast

def struct_byteorder(doc):
    byteorder_xml = doc.findall("byte_order")
    if len(byteorder_xml) >= 1:
        assert len(byteorder_xml) == 1, "`structure.byte_order` is defined too many times!"
        if byteorder_xml[0].text not in ["as_host", "big_endian", "little_endian"]:
            raise ValueError("the specified `byte_order` is not valid: %s"%byteorder_xml[0].text)
        return byteorder_xml[0].text
    else:
        #default value
        return "big_endian"

def header_idfield(header_doc):
    idfield_xml = header_doc.findall("id_field_name")
    assert len(idfield_xml) == 1, "the `header.id_field_name` is not defined in the source file."
    return idfield_xml[0].text  

def parse_enum_pair(enum_keyvalue_doc):
    ast = {"name": enum_keyvalue_doc.text, "id":None}

    #IDs have to be decimal or hexadecimal.
    try:
        ast["id"] = int(enum_keyvalue_doc.attrib["id"])
    except ValueError:
        try:
            ast["id"] = int(enum_keyvalue_doc.attrib["id"], 16)
        except ValueError:
            raise ValueError("the given ID for value {0} is"
                             " not decimal or hexadecimal: {1}".format(ast["name"],
                                enum_keyvalue_doc.attrib["id"]))
    return ast

def parse_enum(enum_doc):
    enum_ast = {
        "values":[],
        "name": enum_doc.findall("name")[0].text
    }

    try:
        enum_ast["size"] = int(enum_doc.findall("size")[0].text)
        assert 1 <= enum_ast["size"] <= 32
    except IndexError:
        enum_ast["size"] = 32

    for value_doc in enum_doc.findall("values/value"):
        enum_ast["values"].append(parse_enum_pair(value_doc))

    return enum_ast

def protocol_info(doc):
    protocol_info = {"proto_name": None, "proto_short": None}
    try:
        protocol_info["proto_name"] = doc.findall("protocolname")[-1].text
    except IndexError:
        raise ValueError("`protocol/protocolname` value cannot be found. Please review the XML document.")

    try:
        protocol_info["proto_short"] = doc.findall("protocolshort")[-1].text
    except IndexError:
        if protocol_info["proto_name"].count(" "):
            protocol_info["proto_short"] = "".join(chunk[0] for chunk in protocol_info["proto_name"].split(" ") if chunk)
        else:
            protocol_info["proto_short"] = protocol_info["proto_name"]

    return protocol_info

def struct_info(struct_doc):
    struct_ast = dict()
    struct_ast["name"]       = structure_name(struct_doc)
    struct_ast["fields"]     = parse_fields(struct_doc)
    try:
        struct_ast["struct_id"]  = structure_id(struct_doc)
    except AssertionError: #we got an header. silly us.
        struct_ast["struct_id"]  = None
    struct_ast["byte_order"] = struct_byteorder(struct_doc)
    return struct_ast

def header_info(doc):
    header_doc = doc.findall("header")[0]
    header_info = struct_info(header_doc)
    header_info["id_field_name"] = header_idfield(header_doc)
    return header_info

def structures_info(doc):
    return [struct_info(struct_doc) for struct_doc in doc.findall("structures/structure")]

def global_enums(doc):
    return [parse_enum(enum_doc) for enum_doc in doc.findall("enums/enum")]

def build_ast(doc):
    ast = dict()
    ast["proto"]      = protocol_info(doc)
    ast["enums"]      = global_enums(doc)
    ast["header"]     = header_info(doc)
    ast["structures"] = structures_info(doc)
    return ast

def parse(str_):
    root = _getroot(str_)
    ast = build_ast(root)

    return ast
