import unittest
from nbt2yaml import parse_nbt
from tests import datafile

class ParseNBTTest(unittest.TestCase):
    def test_basic(self):
        print parse_nbt(datafile("test.nbt"))

    def test_large(self):
        print parse_nbt(datafile("bigtest.nbt"))