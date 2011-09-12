import yaml
from nbt2yaml import parse

explicit_types = parse.TAG_Short, parse.TAG_Long, parse.TAG_Double, parse.TAG_Byte, parse.TAG_Byte_Array
class ForceType(object):
    """Represent a data value with an explicit type.
    
    This is used to output 'short', 'long', 'double', 'byte'
    explicitly, so that we can differentiate on the
    yaml parsing side what specific NBT form to use.
    
    """
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

def _type_representer(dumper, struct):
    if struct.type is parse.TAG_Byte_Array:
        representation = struct.value
    else:
        representation = repr(struct.value)
    return dumper.represent_scalar(u'!%s' % struct.type.name, representation, style='""')

yaml.add_representer(ForceType, _type_representer)

def _type_constructor(type_):
    def _constructor(loader, node):
        value = loader.construct_scalar(node)
        return ForceType(type_, value)
    return _constructor

for type_ in explicit_types:
    yaml.add_constructor(u'!%s' % type_.name, _type_constructor(type_))

def yaml_serialize(struct):
    tag, name, data = struct.type, struct.name, struct.data
    name = name.encode('utf-8')
    return {name:_value_as_yaml(tag, data)}

def _value_as_yaml(type_, value):
    if type_ is parse.TAG_Compound:
        return [yaml_serialize(s) for s in value]
    elif type_ is parse.TAG_String:
        return value.encode('utf-8')
    elif type_ in explicit_types:
        return ForceType(type_, value)
    elif type_ is parse.TAG_List:
        element_type, data = value
        return [_value_as_yaml(element_type, d) for d in data]
    else:
        return value

def _yaml_as_value(type_, value):
    if type_ is parse.TAG_Compound:
        return [yaml_deserialize(s) for s in value]
    elif type_ is parse.TAG_String:
        return value.decode('utf-8')
    elif type_ in explicit_types:
        if type_ in (parse.TAG_Long,):
            return long(value.value)
        elif type_ in (parse.TAG_Int, parse.TAG_Short, parse.TAG_Byte):
            return int(value.value)
        elif type_ in (parse.TAG_Float, parse.TAG_Double):
            return float(value.value)
        else:
            return value.value
    elif type_ is parse.TAG_List:
        ltype = _type_from_yaml(value[0])
        return (ltype, [_yaml_as_value(ltype, s) for s in value])
    else:
        return value

def _type_from_yaml(data):
    if isinstance(data, list):
        if isinstance(data[0], dict):
            type_ = parse.TAG_Compound
        else:
            type_ = parse.TAG_List
    elif isinstance(data, ForceType):
        type_ = data.type
    elif type(data) in canned_types:
        type_ = canned_types[type(data)]
    else:
        raise ValueError("Can't determine type for element: %r" % (data))
    return type_

canned_types = {
    str:parse.TAG_String,
    float:parse.TAG_Float,
    int:parse.TAG_Int,
}

def yaml_deserialize(struct):
    name, data = struct.items()[0]
    type_ = _type_from_yaml(data)

    return parse.Tag._tuple(type_, name.decode('utf-8'), _yaml_as_value(type_, data))

def dump_yaml(struct, canonical=False, default_flow_style=False):
    return yaml.dump(
                yaml_serialize(struct), 
                default_flow_style=default_flow_style, 
                canonical=canonical)


def parse_yaml(stream):
    struct = yaml.load(stream)
    return yaml_deserialize(struct)
