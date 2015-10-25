def build_field(field_ast):
    modifiers = []

    if field_ast.get("no_statement", None):
        modifiers.append("ns="+field_ast["no_statement"])

    return "{}{} {};".format(field_ast["type"], "{"+",".join(modifiers)+"}", field_ast["name"])

def build(ast):
    raise NotImplementedError("Wireshark builder")
