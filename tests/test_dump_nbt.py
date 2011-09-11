import unittest
from nbt2yaml import parse_nbt, dump_nbt
from tests import datafile, eq_
import gzip
import StringIO

class DumpNBTTest(unittest.TestCase):
    def _assert_data(self, fname):
        unzipped_data = gzip.GzipFile(fileobj=datafile(fname)).read()
        parsed = parse_nbt(datafile(fname))
        out = StringIO.StringIO()
        dump_nbt(parsed, out)
        eq_(unzipped_data, out.getvalue())

    def test_basic(self):
        self._assert_data("test.nbt")

    def test_large(self):
        self._assert_data("bigtest.nbt")
