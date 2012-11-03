import unittest
from nbt2yaml import parse_nbt, parse
from tests import datafile, eq_
import struct

class ParseNBTTest(unittest.TestCase):
    def test_basic(self):
        assert_ = (
                    parse.TAG_Compound,
                    u'hello world',
                    [(parse.TAG_String, u'name', u'Bananrama')]
                )
        eq_(parse_nbt(datafile("test.nbt")), assert_)

    def test_lists(self):
        assert_ = (
            parse.TAG_Compound, u'', [
                (parse.TAG_Compound, u'Data', [
                        (parse.TAG_Byte, u'thundering', 0),
                        (parse.TAG_Long, u'LastPlayed', 1315921966180),
                        (parse.TAG_Compound, u'Player', [
                                (parse.TAG_List, u'Motion', (parse.TAG_Double, [
                                            9.166176096485612e-17,
                                            -0.0784000015258789,
                                            -2.063101401779548e-16
                                            ])),
                                (parse.TAG_Short, u'Health', 20),
                                (parse.TAG_List, u'Inventory', (parse.TAG_Byte, []))
                                ])
                        ])
                ])

    def test_large(self):
        assert_ = (
                    parse.TAG_Compound, u'Level', [
                        (parse.TAG_Long, u'longTest', 9223372036854775807L),
                        (parse.TAG_Short, u'shortTest', 32767),
                        (parse.TAG_String, u'stringTest', u'HELLO WORLD THIS IS A TEST STRING \xc5\xc4\xd6!'),
                        (parse.TAG_Float, u'floatTest', 0.4982314705848694),
                        (parse.TAG_Int, u'intTest', 2147483647),
                        (parse.TAG_Compound, u'nested compound test',
                            [
                                (parse.TAG_Compound, u'ham',
                                    [
                                        (parse.TAG_String, u'name', u'Hampus'),
                                        (parse.TAG_Float, u'value', 0.75)
                                    ]),
                                    (parse.TAG_Compound, u'egg',
                                    [
                                        (parse.TAG_String, u'name', u'Eggbert'),
                                        (parse.TAG_Float, u'value', 0.5)
                                    ])
                                ]),
                                (parse.TAG_List, u'listTest (long)', (parse.TAG_Long, [11, 12, 13, 14, 15])),
                    (parse.TAG_List, u'listTest (compound)',
                        (parse.TAG_Compound, [
                            [
                                (parse.TAG_String, u'name', u'Compound tag #0'),
                                (parse.TAG_Long, u'created-on', 1264099775885L)
                            ],
                            [
                                (parse.TAG_String, u'name', u'Compound tag #1'),
                                (parse.TAG_Long, u'created-on', 1264099775885L)
                            ]
                        ])),
                        (parse.TAG_Byte, u'byteTest', 127),
                        (parse.TAG_Byte_Array,
                            u'byteArrayTest (the first 1000 values of '
                                    '(n*n*255+n*7)%100, starting with n=0 '
                                    '(0, 62, 34, 16, 8, ...))',
                                    ''.join([struct.pack('>b', (n*n*255+n*7)%100) for n in xrange(0, 1000)])
                            ),
                        (parse.TAG_Double, u'doubleTest', 0.4931287132182315)
                    ])
        eq_(parse_nbt(datafile("bigtest.nbt")), assert_)

    def test_schematic(self):
        assert_ = (
            parse.TAG_Compound, u'Schematic', [
                (parse.TAG_Byte_Array, u'Blocks', '\x34'),
                (parse.TAG_Short, u'Width', 1),
                (parse.TAG_Short, u'Height', 1),
                (parse.TAG_List, u'Entities', (parse.TAG_Byte, [])),
                (parse.TAG_Short, u'Length', 1),
                (parse.TAG_String, u'Materials', u'Alpha'),
                (parse.TAG_List, u'TileEntities', (parse.TAG_Compound, [
                            [
                                (parse.TAG_Short, u'Delay', 120),
                                (parse.TAG_Int, u'y', 0),
                                (parse.TAG_Int, u'x', 0),
                                (parse.TAG_String, u'EntityId', u'Skeleton'),
                                (parse.TAG_Int, u'z', 0),
                                (parse.TAG_String, u'id', u'MobSpawner')
                                ]
                            ])),
                (parse.TAG_Byte_Array, u'Data', '\x00')
                ])
        
    def test_int_array(self):
        assert_ = (
                    parse.TAG_Compound, 'Test root compound',
                    [(parse.TAG_Int_Array,
                            'Test integer array',
                            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                            12, 13, 14, 15, 16])])
        eq_(parse_nbt(datafile("intarraytest.nbt")), assert_)
