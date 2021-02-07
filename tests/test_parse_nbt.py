import struct

from nbt2yaml import compat
from nbt2yaml import parse
from nbt2yaml import parse_nbt
from . import datafile
from . import eq_


def test_basic():
    assert_ = (
        parse.TAG_Compound,
        "hello world",
        [(parse.TAG_String, "name", "Bananrama")],
    )
    with datafile("test.nbt") as file_:
        eq_(parse_nbt(file_), assert_)


def test_lists():
    assert_ = (
        parse.TAG_Compound,
        "",
        [
            (
                parse.TAG_Compound,
                "Data",
                [
                    (parse.TAG_Byte, "thundering", 0),
                    (parse.TAG_Long, "LastPlayed", 1315921966180),
                    (
                        parse.TAG_Compound,
                        "Player",
                        [
                            (
                                parse.TAG_List,
                                "Motion",
                                (
                                    parse.TAG_Double,
                                    [
                                        9.166176096485612e-17,
                                        -0.0784000015258789,
                                        -2.063101401779548e-16,
                                    ],
                                ),
                            ),
                            (parse.TAG_Short, "Health", 20),
                            (
                                parse.TAG_List,
                                "Inventory",
                                (parse.TAG_Byte, []),
                            ),
                        ],
                    ),
                ],
            )
        ],
    )
    with datafile("list.nbt") as file_:
        eq_(parse_nbt(file_), assert_)


def test_large():
    assert_ = (
        parse.TAG_Compound,
        "Level",
        [
            (parse.TAG_Long, "longTest", 9223372036854775807),
            (parse.TAG_Short, "shortTest", 32767),
            (
                parse.TAG_String,
                "stringTest",
                compat.ue("HELLO WORLD THIS IS A TEST STRING \xc5\xc4\xd6!"),
            ),
            (parse.TAG_Float, "floatTest", 0.4982314705848694),
            (parse.TAG_Int, "intTest", 2147483647),
            (
                parse.TAG_Compound,
                "nested compound test",
                [
                    (
                        parse.TAG_Compound,
                        "ham",
                        [
                            (parse.TAG_String, "name", "Hampus"),
                            (parse.TAG_Float, "value", 0.75),
                        ],
                    ),
                    (
                        parse.TAG_Compound,
                        "egg",
                        [
                            (parse.TAG_String, "name", "Eggbert"),
                            (parse.TAG_Float, "value", 0.5),
                        ],
                    ),
                ],
            ),
            (
                parse.TAG_List,
                "listTest (long)",
                (parse.TAG_Long, [11, 12, 13, 14, 15]),
            ),
            (
                parse.TAG_List,
                "listTest (compound)",
                (
                    parse.TAG_Compound,
                    [
                        [
                            (parse.TAG_String, "name", "Compound tag #0"),
                            (parse.TAG_Long, "created-on", 1264099775885),
                        ],
                        [
                            (parse.TAG_String, "name", "Compound tag #1"),
                            (parse.TAG_Long, "created-on", 1264099775885),
                        ],
                    ],
                ),
            ),
            (parse.TAG_Byte, "byteTest", 127),
            (
                parse.TAG_Byte_Array,
                "byteArrayTest (the first 1000 values of "
                "(n*n*255+n*7)%100, starting with n=0 "
                "(0, 62, 34, 16, 8, ...))",
                b"".join(
                    [
                        struct.pack(">b", (n * n * 255 + n * 7) % 100)
                        for n in compat.range(0, 1000)
                    ]
                ),
            ),
            (parse.TAG_Double, "doubleTest", 0.4931287132182315),
        ],
    )

    with datafile("bigtest.nbt") as file_:
        eq_(parse_nbt(file_), assert_)


def test_schematic():
    assert_ = (
        parse.TAG_Compound,
        "Schematic",
        [
            (parse.TAG_Byte_Array, "Blocks", b"\x34"),
            (parse.TAG_Short, "Width", 1),
            (parse.TAG_Short, "Height", 1),
            (parse.TAG_List, "Entities", (parse.TAG_Byte, [])),
            (parse.TAG_Short, "Length", 1),
            (parse.TAG_String, "Materials", "Alpha"),
            (
                parse.TAG_List,
                "TileEntities",
                (
                    parse.TAG_Compound,
                    [
                        [
                            (parse.TAG_Short, "Delay", 120),
                            (parse.TAG_Int, "y", 0),
                            (parse.TAG_Int, "x", 0),
                            (parse.TAG_String, "EntityId", "Skeleton"),
                            (parse.TAG_Int, "z", 0),
                            (parse.TAG_String, "id", "MobSpawner"),
                        ]
                    ],
                ),
            ),
            (parse.TAG_Byte_Array, "Data", b"\x00"),
        ],
    )
    with datafile("spawner.nbt") as file_:
        eq_(parse_nbt(file_), assert_)


def test_int_array():
    assert_ = (
        parse.TAG_Compound,
        "Test root compound",
        [
            (
                parse.TAG_Int_Array,
                "Test integer array",
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
            )
        ],
    )
    with datafile("intarraytest.nbt") as file_:
        eq_(parse_nbt(file_), assert_)
