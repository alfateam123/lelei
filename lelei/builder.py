import pystache

STRUCT_TEMPLATE = """
struct {{struct_name}}
{
    {{#fields}}
    {{.}}
    {{/fields}}
}
""".strip()

def build_field(field_ast):
    return pystache.render("{{type}} {{name}};", field_ast)

def build_struct(ast):
    fields = (build_field(f_) for f_ in ast["fields"])
    return pystache.render(STRUCT_TEMPLATE, struct_name=ast["name"], fields=fields)

def build_fdesc(ast):
    return build_struct(ast)

