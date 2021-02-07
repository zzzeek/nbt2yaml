import unittest

from nbt2yaml import compat
from nbt2yaml import dump_nbt
from nbt2yaml import parse_nbt
from nbt2yaml import parse_yaml
from nbt2yaml.compat import BytesIO
from . import datafile
from . import eq_


class FromYamlTest(unittest.TestCase):
    def test_basic(self):
        with datafile("test.yml") as file_:
            data = parse_yaml(file_)

        self._assert(data, "test.nbt")

    def test_large(self):
        if not compat.py3k:
            filename = "bigtest.py2k.yml"
        else:
            filename = "bigtest.yml"
        with datafile(filename) as file_:
            data = parse_yaml(file_)
        self._assert(data, "bigtest.nbt")

    def test_lists(self):
        with datafile("list.yml") as file_:
            data = parse_yaml(file_)
        self._assert(data, "list.nbt")

    def test_spawner(self):
        with datafile("spawner.yml") as file_:
            data = parse_yaml(file_)
        self._assert(data, "spawner.nbt")

    def test_int_array(self):
        with datafile("intarraytest.yml") as file_:
            data = parse_yaml(file_)
        self._assert(data, "intarraytest.nbt")

    def test_long_array(self):
        with datafile("longarraytest.yml") as file_:
            data = parse_yaml(file_)
        self._assert(data, "longarraytest.nbt")

    def test_chunk(self):
        with datafile("chunk.yml") as file_:
            data = parse_yaml(file_)
        self._assert(data, "chunk.nbt")

    def _assert(self, data, nbt_filename):
        with datafile(nbt_filename) as file_:
            eq_(data, parse_nbt(file_))

        out = BytesIO()
        dump_nbt(data, out, gzipped=False)

        with datafile(nbt_filename, ungzip=True) as file_:
            eq_(out.getvalue(), file_.read())
