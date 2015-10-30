import pystache
import re

ENUM_TEMPLATE = """
enum{{ast.size}} {{ast.name}}
{
  {{#values}}
  {{.}}
  {{/values}}
}
""".strip()

STRUCT_TEMPLATE = """
struct {{struct_name}}
{
    {{byte_order}}
    {{header_field}}
    {{#fields}}
    {{.}}
    {{/fields}}
}
""".strip()

WSDG_TEMPLATE = """
PROTONAME      {{proto.proto_name}}
PROTOSHORTNAME {{proto.proto_short}}
PROTOABBREV    {{proto.proto_short}}

PARENT_SUBFIELD        tcp.port
PARENT_SUBFIELD_VALUES 20127

MSG_HEADER_TYPE   {{header.name}}
MSG_ID_FIELD_NAME {{header.id_field_name}}

MSG_MAIN_TYPE T_msg_switch({{header.id_field_name}})

PROTO_TYPE_DEFINITIONS

include {{fname}}.fdesc ;
""".strip()

FIELD_TMPL = "{{type}} {{name}};"

SWITCH_TMPL = """
switch T_msg_switch T_type_messages
{
  {{#values}}
  {{.}}
  {{/values}}
}
"""

SWITCH_CASE_TMPL = "case T_type_messages::{{struct_name}}_t : {{struct_name}} \"\";"

def build_simple_field(type_, name_):
    return pystache.render(FIELD_TMPL, type=type_, name=name_)

def build_simple_enum(type_, name_):
    return pystache.render("{{type}} {{name}}", type=type_, name=name_)

def build_field(field_ast):
    type_ = field_ast["type"]
    try:
        type_ += "[{0}]".format(field_ast["repeated"]) if field_ast["repeated"]>1 else ""
    except TypeError: #comparing strings and ints
        type_ += "[{0}]".format(field_ast["repeated"])
    return pystache.render("{{type}} {{name}};", field_ast, type=type_)

def build_struct(struct_ast, header_type_name=None):
    fields = (build_field(f_) for f_ in struct_ast["fields"])
    header_field    = build_simple_field(header_type_name, "header") if header_type_name else ""
    byteorder_field = build_simple_field("byte_order", struct_ast["byte_order"])
    return pystache.render(STRUCT_TEMPLATE,
                           header_field=header_field,
                           struct_name=struct_ast["name"],
                           byte_order=byteorder_field,
                           fields=fields)

def build_enum(enum_ast):
    #one day, I'll understand how to do the same thing using mustache only.
    values = [build_simple_enum(type_=value_ast["name"], name_=value_ast["id"]) for value_ast in enum_ast["values"]]
    return pystache.render(ENUM_TEMPLATE, ast=enum_ast, values=values)

def build_type_messages(ast):
    id_field_name = ast["header"]["id_field_name"]
    #incidentally, an IndexError will be raised here.
    #It should be done during the parsing phase, but nobody is perfect :)
    id_field_type = [f_ for f_ in ast["header"]["fields"]
                     if f_["name"] == id_field_name ][0]["type"]
    ids_list = [build_simple_enum(type_=struct_ast["name"]+"_t", name_=struct_ast["struct_id"])
                  for struct_ast in ast["structures"]]
    return pystache.render(ENUM_TEMPLATE, ast={
                                          "size": re.findall("(\d+)$", id_field_type)[0],
                                          "name": "T_type_messages"
                                          }, values=ids_list)

def build_type_switch(ast):
    # return NotImplementedError(ast)
    id_field_name = ast["header"]["id_field_name"]
    #incidentally, an IndexError will be raised here.
    #It should be done during the parsing phase, but nobody is perfect :)
    id_field_type = [field for field in ast["header"]["fields"]
                     if field["name"]==id_field_name][0]["type"]
    ids_list = [(struct_ast["name"], struct_ast["struct_id"])
                  for struct_ast in ast["structures"]]
    return pystache.render(SWITCH_TMPL,
      values = [pystache.render(SWITCH_CASE_TMPL,struct_name=id_[0])
                  for id_ in ids_list]).replace("&quot;", '"')


def build_fdesc(ast):
    type_messages_content = build_type_messages(ast)
    header_content     = build_struct(ast["header"])
    enums_content      = "\n".join(build_enum(enum_ast) for enum_ast in ast["enums"])
    structures_content = "\n".join(build_struct(struct_ast, ast["header"]["name"]) for struct_ast in ast["structures"])
    switch_messages    = build_type_switch(ast)
    return "\n".join([type_messages_content,
                      enums_content,
                      header_content,
                      structures_content,
                      switch_messages])


def build_wsgd(ast, proto_name):
    return pystache.render(WSDG_TEMPLATE,
                           ast, fname=proto_name)
