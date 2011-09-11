import unittest
from nbt2yaml import parse_nbt, to_yaml
from tests import datafile

class ToYamlTest(unittest.TestCase):
    def test_basic(self):
        data = parse_nbt(datafile("test.nbt"))
        print "\n", to_yaml(data)

    def test_large(self):
        data = parse_nbt(datafile("bigtest.nbt"))
        print "\n", to_yaml(data)
