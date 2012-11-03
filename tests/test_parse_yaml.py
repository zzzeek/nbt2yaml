import unittest
from nbt2yaml import parse_nbt, dump_yaml, parse_yaml, dump_nbt
from tests import datafile, eq_

# TODO: this is to avoid ascii decode issues, is a huge hack.  need a
# real binary buffer object
import cStringIO as StringIO

class FromYamlTest(unittest.TestCase):
    def test_basic(self):
        data = parse_yaml(datafile("test.yml"))

        self._assert(data, "test.nbt")

    def test_large(self):
        data = parse_yaml(datafile("bigtest.yml"))
        self._assert(data, "bigtest.nbt")


    def test_lists(self):
        data = parse_yaml(datafile("list.yml"))
        self._assert(data, "list.nbt")


    def test_spawner(self):
        data = parse_yaml(datafile("spawner.yml"))
        self._assert(data, "spawner.nbt")

    def test_int_array(self):
        data = parse_yaml(datafile("intarraytest.yml"))
        self._assert(data, "intarraytest.nbt")

    def test_chunk(self):
        data = parse_yaml(datafile("chunk.yml"))
        self._assert(data, "chunk.nbt")

    def _assert(self, data, nbt_filename):
        eq_(data, parse_nbt(datafile(nbt_filename)))

        out = StringIO.StringIO()
        dump_nbt(data, out, gzipped=False)

        eq_(out.getvalue(), datafile(nbt_filename, ungzip=True).read())
