import gzip
import unittest

from nbt2yaml import dump_nbt
from nbt2yaml import parse_nbt
from nbt2yaml.compat import BytesIO
from . import datafile
from . import eq_


class DumpNBTTest(unittest.TestCase):
    def _assert_data(self, fname):
        with datafile(fname) as df:
            unzipped_data = gzip.GzipFile(fileobj=df).read()

        with datafile(fname) as df:
            parsed = parse_nbt(df)

        out = BytesIO()
        dump_nbt(parsed, out)
        out = gzip.GzipFile(fileobj=BytesIO(out.getvalue())).read()
        eq_(unzipped_data, out)

    def test_basic(self):
        self._assert_data("test.nbt")

    def test_lists(self):
        self._assert_data("list.nbt")

    def test_large(self):
        self._assert_data("bigtest.nbt")

    def test_spawner(self):
        self._assert_data("spawner.nbt")

    def test_int_array(self):
        self._assert_data("intarraytest.nbt")

    def test_long_array(self):
        self._assert_data("longarraytest.nbt")

    def test_chunk(self):
        self._assert_data("chunk.nbt")
