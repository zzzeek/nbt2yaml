import unittest
from nbt2yaml import parse_nbt, dump_yaml
from tests import datafile, eq_

class ToYamlTest(unittest.TestCase):
    def test_basic(self):
        data = parse_nbt(datafile("test.nbt"))
        eq_(dump_yaml(data), datafile("test.yml").read())

    def test_lists(self):
        data = parse_nbt(datafile("list.nbt"))
        eq_(dump_yaml(data), datafile("list.yml").read())

    def test_spawner(self):
        data = parse_nbt(datafile("spawner.nbt"))
        eq_(dump_yaml(data), datafile("spawner.yml").read())

    def test_int_array(self):
        data = parse_nbt(datafile("intarraytest.nbt"))
        eq_(dump_yaml(data), datafile("intarraytest.yml").read())

    def test_large(self):
        data = parse_nbt(datafile("bigtest.nbt"))
        eq_(dump_yaml(data), datafile("bigtest.yml").read())

    def test_chunk(self):
        data = parse_nbt(datafile("chunk.nbt"))
        eq_(dump_yaml(data), datafile("chunk.yml").read())
