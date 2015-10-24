def build_field(field_ast):
	return "{} {};".format(field_ast["type"], field_ast["name"])

def build(ast):
    raise NotImplementedError("Wireshark builder")
