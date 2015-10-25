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

#PROTO_TYPE_DEFINITIONS

include {{fname}}.fdesc ;
""".strip()

def build_field(field_ast):
    return pystache.render("{{type}} {{name}};", field_ast)

def build_struct(ast):
    fields = (build_field(f_) for f_ in ast["fields"])
    return pystache.render(STRUCT_TEMPLATE, struct_name=ast["name"], fields=fields)

def build_fdesc(ast):
    return build_struct(ast)

def build_wsgd(ast, proto_name):
    #proto_info = ast["protocol_info"]
    return pystache.render(WSDG_TEMPLATE,
                           ast, fname=proto_name)
