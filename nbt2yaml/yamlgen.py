import yaml
from nbt2yaml import parse

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
    return dumper.represent_scalar(u'!%s' % struct.type, repr(struct.value), style='""')

yaml.add_representer(ForceType, _type_representer)

def yaml_serialize(struct):
    tag, name, data = struct.type, struct.name, struct.data
    name = name.encode('utf-8')
    return {name:_value_as_yaml(tag, data)}

def _value_as_yaml(type_, value):
    if type_ is parse.TAG_Compound:
        return [yaml_serialize(s) for s in value]
    elif type_ is parse.TAG_String:
        return value.encode('utf-8')
    elif type_ in (parse.TAG_Short, parse.TAG_Long, parse.TAG_Double, parse.TAG_Byte):
        return ForceType(type_.name, value)
    elif type_ is parse.TAG_List:
        element_type, data = value
        return [_value_as_yaml(element_type, d) for d in data]
    else:
        return value

def to_yaml(struct, canonical=False, default_flow_style=False):
    return yaml.dump(
                yaml_serialize(struct), 
                default_flow_style=default_flow_style, 
                canonical=canonical)
