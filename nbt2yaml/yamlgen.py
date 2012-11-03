import yaml
from nbt2yaml import parse

_explicit_types = parse.TAG_Short, parse.TAG_Long, parse.TAG_Double, parse.TAG_Byte, parse.TAG_Byte_Array
_all_types = parse.Tag._tags.values()

_canned_types = {
    str:parse.TAG_String,
    float:parse.TAG_Float,
    int:parse.TAG_Int,
}

_types_to_python = {
    parse.TAG_Long:long,
    parse.TAG_Int:int,
    parse.TAG_Short:int,
    parse.TAG_Byte:int,
    parse.TAG_Float:float,
    parse.TAG_Double:float
}

class ForceType(object):
    """Represent a data value with an explicit type.
    
    This is used to output 'short', 'long', 'double', 'byte'
    explicitly, so that we can differentiate on the
    yaml parsing side what specific NBT form to use.
    
    """
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

class ForceListOfType(ForceType):
    pass

class ForceIntArray(ForceType):
    pass

def _hex_dump(binary):
    hexa = []
    for i in binary:
        hexa.append("{0:02X}".format(ord(i)))
    return ' '.join(hexa)

def _hex_undump(hexa):
    binary = ""
    hexa = hexa.split(' ') # I did not want to import the re module
    for i in hexa:
        current = int(i, 16)
        binary += chr(current)
    return binary

def _type_representer(dumper, struct):
    if struct.type is parse.TAG_Byte_Array:
        representation = _hex_dump(struct.value)
    else:
        representation = repr(struct.value)
    return dumper.represent_scalar(u'!%s' % struct.type.name, representation, style='""')

def _collection_representer(dumper, struct):
    return dumper.represent_sequence(u'!list_%s' % struct.type.name, struct.value)

def _int_array_representer(dumper, struct):
    return dumper.represent_sequence(u'!int_array', struct.value)

yaml.add_representer(ForceType, _type_representer)
yaml.add_representer(ForceListOfType, _collection_representer)
yaml.add_representer(ForceIntArray, _int_array_representer)

def _type_constructor(type_):
    def _constructor(loader, node):
        value = loader.construct_scalar(node)
        return ForceType(type_, value)
    return _constructor

def _list_constructor(type_):
    def _constructor(loader, node):
        value = loader.construct_sequence(node)
        return ForceListOfType(type_, value)
    return _constructor

def _int_array_constructor(loader, node):
    value = loader.construct_sequence(node)
    return ForceIntArray(parse.TAG_Int_Array, value)

def _byte_array_constructor(loader, node):
    value = loader.construct_scalar(node)
    return ForceType(parse.TAG_Byte_Array, _hex_undump(value))

for type_ in _explicit_types:
    if not type is parse.TAG_Byte_Array:
        yaml.add_constructor(u'!%s' % type_.name, _type_constructor(type_))

for type_ in _all_types:
    yaml.add_constructor(u'!list_%s' % type_.name, _list_constructor(type_))

yaml.add_constructor(u'!int_array', _int_array_constructor)
yaml.add_constructor(u'!byte_array', _byte_array_constructor)

def _yaml_serialize(struct):
    tag, name, data = struct.type, struct.name, struct.data
    name = name.encode('utf-8')
    return {name:_value_as_yaml(tag, data)}

def _yaml_deserialize(struct):
    name, data = struct.items()[0]
    type_ = _type_from_yaml(data)
    return parse.Tag._tuple(type_, name.decode('utf-8'), _yaml_as_value(type_, data))

def _value_as_yaml(type_, value):
    if type_ is parse.TAG_Compound:
        return [_yaml_serialize(s) for s in value]
    elif type_ is parse.TAG_String:
        return value.encode('utf-8')
    elif type_ in _explicit_types:
        return ForceType(type_, value)
    elif type_ is parse.TAG_List:
        element_type, data = value
        return ForceListOfType(element_type, [_value_as_yaml(element_type, d) for d in data])
    elif type_ is parse.TAG_Int_Array:
        return ForceIntArray(parse.TAG_Int, value)
    else:
        return value

def _yaml_as_value(type_, value):
    if type_ is parse.TAG_Compound:
        return [_yaml_deserialize(s) for s in value]
    elif type_ is parse.TAG_String:
        return value.decode('utf-8')
    elif type_ in _explicit_types:
        if type_ in _types_to_python:
            return _types_to_python[type_](value.value)
        else:
            return value.value
    elif type_ is parse.TAG_List:
        ltype = value.type
        return (ltype, [_yaml_as_value(ltype, s) for s in value.value])
    elif type_ is parse.TAG_Int_Array:
        return value.value
    else:
        return value

def _type_from_yaml(data):
    if isinstance(data, ForceListOfType):
        return parse.TAG_List
    elif isinstance(data, ForceIntArray):
        return parse.TAG_Int_Array
    elif isinstance(data, list):
        assert data and isinstance(data[0], dict)
        return parse.TAG_Compound
    elif isinstance(data, ForceType):
        return data.type
    elif type(data) in _canned_types:
        return _canned_types[type(data)]
    else:
        raise ValueError("Can't determine type for element: %r" % data)

def dump_yaml(struct, canonical=False, default_flow_style=False):
    """Dump a yaml string given an nbt structure parsed by nbt2yaml."""

    return yaml.dump(
                _yaml_serialize(struct), 
                default_flow_style=default_flow_style, 
                canonical=canonical)


def parse_yaml(stream):
    """Parse a yaml stream into an nbt structure readable by nbt2yaml."""

    return _yaml_deserialize(yaml.load(stream))
