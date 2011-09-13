import unittest
from nbt2yaml import parse_nbt, dump_yaml, parse_yaml, dump_nbt
from tests import datafile, eq_

class FromYamlTest(unittest.TestCase):
    def test_basic(self):
        data = parse_yaml(datafile("test.yml"))

        eq_(data, parse_nbt(datafile("test.nbt")))

    def test_large(self):
        data = parse_yaml(datafile("bigtest.yml"))

        eq_(data, parse_nbt(datafile("bigtest.nbt")))

    def test_lists(self):
        data = parse_yaml(datafile("list.yml"))

        eq_(data, parse_nbt(datafile("list.nbt")))