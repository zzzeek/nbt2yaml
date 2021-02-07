import pytest

from nbt2yaml import compat
from nbt2yaml import dump_nbt
from nbt2yaml import parse_nbt
from nbt2yaml import parse_yaml
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
def test_from_yaml(name):
    nbt_name = "%s.nbt" % name
    yml_name = "%s.yml" % name

    if not compat.py3k and yml_name == "bigtest.yml":
        yml_name = "bigtest.py2k.yml"

    with datafile(yml_name) as file_:
        data = parse_yaml(file_)

    with datafile(nbt_name) as file_:
        eq_(data, parse_nbt(file_))

    out = BytesIO()
    dump_nbt(data, out, gzipped=False)

    with datafile(nbt_name, ungzip=True) as file_:
        eq_(out.getvalue(), file_.read())
