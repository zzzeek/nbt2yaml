import struct
import gzip
from collections import namedtuple

class Tag(object):
    _tags = {}
    _tuple = namedtuple("Tag", ["type", "name", "data"])

    def __init__(self, name, id):
        self.name = name
        Tag._tags[id] = self

    @classmethod
    def from_stream(cls, stream):
        return cls._tags[struct.unpack('>b', stream.read(1))[0]]

    def parse(self, stream):
        name = TAG_String._parse_impl(stream)
        data = self._parse_impl(stream)
        return Tag._tuple(self, name, data)

    def _parse_impl(self):
        raise NotImplementedError()

    def __repr__(self):
        return "TAG_%s" % self.name

class FixedTag(Tag):
    def __init__(self, name, id, size, format):
        Tag.__init__(self, name, id)
        self.size = size
        self.format = format

    def _parse_impl(self, stream):
        return struct.unpack(">" + self.format, stream.read(self.size))[0]

class EndTag(Tag):
    ""

class VariableTag(Tag):
    def __init__(self, name, id, length_tag, encoding=None):
        Tag.__init__(self, name, id)
        self.length_tag = length_tag
        self.encoding = encoding

    def _parse_impl(self, stream):
        length = _data_length(self.length_tag, stream)
        data = stream.read(length)
        if self.encoding:
            data = data.decode(self.encoding)
        return data

class ListTag(Tag):
    def _parse_impl(self, stream):
        element_type = Tag.from_stream(stream)
        length = _data_length(TAG_Int, stream)

        return [
            element_type._parse_impl(stream) for i in xrange(length)
        ]

class CompoundTag(Tag):
    def _parse_impl(self, stream):
        data = []
        while True:
            c_type_ = Tag.from_stream(stream)
            if c_type_ is TAG_End:
                break
            data.append(c_type_.parse(stream))
        return data

TAG_End = EndTag('end', 0)
TAG_Byte = FixedTag('byte', 1, 1, 'b')
TAG_Short = FixedTag('short', 2, 2, 'h')
TAG_Int = FixedTag('int', 3, 4, 'i')
TAG_Long = FixedTag('long', 4, 8, 'q')
TAG_Float = FixedTag('float', 5, 4, 'f')
TAG_Double = FixedTag('double', 6, 8, 'd')
TAG_Byte_Array = VariableTag('byte_array', 7, TAG_Int)
TAG_String = VariableTag('string', 8, TAG_Short, encoding='utf-8')
TAG_List = ListTag('list', 9)
TAG_Compound = CompoundTag('compound', 10)

def _data_length(length_type, stream):
    return struct.unpack(">" + length_type.format, stream.read(length_type.size))[0]

def parse_nbt(stream, gzipped=True):
    if gzipped:
        stream = gzip.GzipFile(fileobj=stream)
    type_ = Tag.from_stream(stream)
    return type_.parse(stream)

