import pytest

from nbt2yaml import compat
from nbt2yaml import dump_yaml
from nbt2yaml import parse_nbt
from . import datafile
from . import eq_
from . import file_as_string


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
def test_to_yaml(name):
    nbt_name = "%s.nbt" % name
    yml_name = "%s.yml" % name

    if not compat.py3k and yml_name == "bigtest.yml":
        yml_name = "bigtest.py2k.yml"

    with datafile(nbt_name) as file_:
        data = parse_nbt(file_)
    eq_(dump_yaml(data), file_as_string(yml_name))
