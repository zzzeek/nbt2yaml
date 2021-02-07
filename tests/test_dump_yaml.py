import unittest

from nbt2yaml import compat
from nbt2yaml import dump_yaml
from nbt2yaml import parse_nbt
from . import datafile
from . import eq_
from . import file_as_string


class ToYamlTest(unittest.TestCase):
    def test_basic(self):
        with datafile("test.nbt") as file_:
            data = parse_nbt(file_)
        eq_(dump_yaml(data), file_as_string("test.yml"))

    def test_lists(self):
        with datafile("list.nbt") as file_:
            data = parse_nbt(file_)
        eq_(dump_yaml(data), file_as_string("list.yml"))

    def test_spawner(self):
        with datafile("spawner.nbt") as file_:
            data = parse_nbt(file_)
        eq_(dump_yaml(data), file_as_string("spawner.yml"))

    def test_int_array(self):
        with datafile("intarraytest.nbt") as file_:
            data = parse_nbt(file_)
        eq_(dump_yaml(data), file_as_string("intarraytest.yml"))

    def test_long_array(self):
        with datafile("longarraytest.nbt") as file_:
            data = parse_nbt(file_)
        eq_(dump_yaml(data), file_as_string("longarraytest.yml"))

    def test_large(self):
        with datafile("bigtest.nbt") as file_:
            data = parse_nbt(file_)

        if not compat.py3k:
            filename = "bigtest.py2k.yml"
        else:
            filename = "bigtest.yml"

        eq_(dump_yaml(data), file_as_string(filename))

    def test_chunk(self):
        with datafile("chunk.nbt") as file_:
            data = parse_nbt(file_)
        eq_(dump_yaml(data), file_as_string("chunk.yml"))
