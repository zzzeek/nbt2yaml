import gzip

import pytest

from nbt2yaml import dump_nbt
from nbt2yaml import parse_nbt
from nbt2yaml.compat import BytesIO
from . import datafile
from . import eq_


@pytest.mark.parametrize(
    "name",
    [
        ("test",),
        ("list",),
        ("bigtest",),
        ("spawner",),
        ("intarraytest",),
        ("longarraytest",),
        ("chunk",),
        ("empty_compound",),
    ],
)
def test_dump_nbt(name):
    nbt_name = "%s.nbt" % name
    with datafile(nbt_name) as df:
        unzipped_data = gzip.GzipFile(fileobj=df).read()

    with datafile(nbt_name) as df:
        parsed = parse_nbt(df)

    out = BytesIO()
    dump_nbt(parsed, out)
    out = gzip.GzipFile(fileobj=BytesIO(out.getvalue())).read()
    eq_(unzipped_data, out)
