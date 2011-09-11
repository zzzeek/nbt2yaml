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
                                    ''.join([struct.pack('>b', (n*n*255+n*7)%100) for n in range(0, 1000)])
                            ),
                        (parse.TAG_Double, u'doubleTest', 0.4931287132182315)
                    ])
        eq_(parse_nbt(datafile("bigtest.nbt")), assert_)
