import pystache

STRUCT_TEMPLATE = """
struct {{struct_name}}
{
    {{#fields}}
    {{.}}
    {{/fields}}
}
""".strip()

WSDG_TEMPLATE = """
PROTONAME      {{proto.proto_name}}
PROTOSHORTNAME {{proto.proto_shortname}}
PROTOABBREV    {{proto.proto_shortname}}

PARENT_SUBFIELD        tcp.port
PARENT_SUBFIELD_VALUES 20127

MSG_HEADER_TYPE   {{header.name}}
MSG_ID_FIELD_NAME {{header.id_field_name}}

#PROTO_TYPE_DEFINITIONS

include {{fname}}.fdesc ;
""".strip()

def build_field(field_ast):
    return pystache.render("{{type}} {{name}};", field_ast)

def build_struct(struct_ast):
    fields = (build_field(f_) for f_ in struct_ast["fields"])
    return pystache.render(STRUCT_TEMPLATE, struct_name=struct_ast["name"], fields=fields)

def build_fdesc(ast):
    header_content = build_struct(ast["header"])
    struct_content = build_struct(ast["struct"])
    return "\n".join([header_content, struct_content])

def build_wsgd(ast, proto_name):
    return pystache.render(WSDG_TEMPLATE,
                           ast, fname=proto_name)
