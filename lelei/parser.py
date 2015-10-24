import xml.sax
import re
from transitions import Machine

class StructureParser(xml.sax.ContentHandler):

    _parsing_states = ['reading', 'inside_fieldlists', 'inside_field', 'inside_name']

    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self._ast = dict()
        self._tempStruct = {"type":None, "bits":-1, "name":None}
        self._prepare_fsm()

    def _prepare_fsm(self):
        self.machine = Machine(model=self,
                               states=StructureParser._parsing_states,
                               initial='reading')
        self.machine.add_transition("found_fieldlists", "reading", "inside_fieldlists")
        self.machine.add_transition("found_field", "inside_fieldlists", "inside_field")
        self.machine.add_transition("found_name",  "reading", "inside_name")
        self.machine.add_transition("exitfrom_name", "inside_name", "reading")
        self.machine.add_transition("exitfrom_field", "inside_field", "inside_fieldlists")
        self.machine.add_transition("exitfrom_fieldlists", "inside_fieldlists", "reading")

    @property
    def ast(self):
        return self._ast.copy()
    
    def characters(self, content):
        #if self._reading_status == INSIDE_NAME:
        if self.state == "inside_name":
            self._ast["name"] = content
        #elif self._reading_status == INSIDE_FIELD:
        elif self.state == "inside_field":
            self._tempStruct["name"] = content

    def startElement(self, name, attrs):
        assert(self.machine)
        if name == "name":
            self.found_name()
            #self._reading_status = INSIDE_NAME 
        elif name == "fields": #and self._reading_status == READING:
            #self._reading_status = INSIDE_FIELDSLIST
            self.found_fieldlists()
        elif name == "field": #and self._reading_status == INSIDE_FIELDSLIST:
            #self._reading_status = INSIDE_FIELD
            self.found_field()
            self._tempStruct["type"] = attrs.getValue("type")
            self._tempStruct["bits"] = self.bitsForStructure(attrs.getValue("type"), int(attrs.getValue("bits")))

    def endElement(self, name):
        if self.state == "inside_name":
            self.exitfrom_name()
        
        elif self.state == "inside_field":
            self.exitfrom_field()
            try:
                self._ast["fields"].append(self._tempStruct.copy())
            except KeyError:
                self._ast["fields"] = [self._tempStruct.copy()]
            self._tempStruct = {"type":None, "bits":-1, "name":None}
        
        elif self.state == "inside_fieldlists":
            self.exitfrom_fieldlists()

    def bitsForStructure(self, struct_type, read_bits):
        #works for int/uint32, etc.
        #we hope you don't want to send floats without converting them to uint32 :D
        bits_by_structType = int(re.findall("(\d+)$", struct_type)[-1])
        assert bits_by_structType%8 == 0 and 0 < bits_by_structType <= 64, "{} is not a valid dimension for a type".format(bits_by_structType)
        if read_bits > bits_by_structType:
            raise ValueError("you are asking for more bits than the type can contain! %s -> %d"%(struct_type, read_bits))
        
        if read_bits == 0:
            return bits_by_structType
        else:
            return read_bits
