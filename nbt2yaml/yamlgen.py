import yaml
from nbt2yaml import parse

class YamlSerialize(object):
    def __init__(self, struct):
        self.tag, self.name, self.data = struct


def _tag_representer(dumper, struct):
    tag, name, data = struct.tag, struct.name, struct.data
    if tag is parse.TAG_Compound:
        data = [YamlSerialize(elem) for elem in data]
    elif tag is parse.TAG_String:
        data = data.encode('utf-8')

    return dumper.represent_mapping(
        u'!%s' % repr(tag), {
            name.encode('utf-8'):data
        },
    )


yaml.add_representer(YamlSerialize, _tag_representer)

def to_yaml(struct):
    print yaml.dump(YamlSerialize(struct))