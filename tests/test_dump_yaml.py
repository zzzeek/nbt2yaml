import unittest
from nbt2yaml import parse_nbt, dump_yaml
from tests import datafile, eq_

class ToYamlTest(unittest.TestCase):
    def test_basic(self):
        data = parse_nbt(datafile("test.nbt"))
        eq_(dump_yaml(data),
"""hello world:
- name: Bananrama
""")

    def test_lists(self):
        data = parse_nbt(datafile("list.nbt"))
        eq_(dump_yaml(data),
"""? ''
: - Data:
    - thundering: !byte "0"
    - LastPlayed: !long "1315921966180"
    - Player:
      - Motion: !list_double
        - !double "9.166176096485612e-17"
        - !double "-0.0784000015258789"
        - !double "-2.063101401779548e-16"
      - Health: !short "20"
      - Inventory: !list_byte []
""")

    def test_spawner(self):
        data = parse_nbt(datafile("spawner.nbt"))
        eq_(dump_yaml(data), datafile("spawner.yml").read())

    def test_large(self):
        data = parse_nbt(datafile("bigtest.nbt"))
        eq_(dump_yaml(data),
r"""Level:
- longTest: !long "9223372036854775807"
- shortTest: !short "32767"
- stringTest: !!python/str "HELLO WORLD THIS IS A TEST STRING \xC5\xC4\xD6!"
- floatTest: 0.4982314705848694
- intTest: 2147483647
- nested compound test:
  - ham:
    - name: Hampus
    - value: 0.75
  - egg:
    - name: Eggbert
    - value: 0.5
- listTest (long): !list_long
  - !long "11"
  - !long "12"
  - !long "13"
  - !long "14"
  - !long "15"
- listTest (compound): !list_compound
  - - name: 'Compound tag #0'
    - created-on: !long "1264099775885"
  - - name: 'Compound tag #1'
    - created-on: !long "1264099775885"
- byteTest: !byte "127"
- byteArrayTest (the first 1000 values of (n*n*255+n*7)%100, starting with n=0 (0, 62, 34, 16, 8, ...)): !byte_array "\0\
    >\"\x10\b\n\x16,L\x12F \x04VNP\\\x0E.X(\x02J802>T\x10:\nH,\x1A\x12\x14 6V\x1C\
    P*\x0E`XZ\x02\x188b2\fTB:<H^\x1AD\x14R6$\x1C\x1E*@`&Z4\x18\x06b\0\f\"B\b<\x16\
    ^LDFR\x04$N\x1E\\@.&(4J\x060\0>\"\x10\b\n\x16,L\x12F \x04VNP\\\x0E.X(\x02J802>T\x10\
    :\nH,\x1A\x12\x14 6V\x1CP*\x0E`XZ\x02\x188b2\fTB:<H^\x1AD\x14R6$\x1C\x1E*@`&Z4\x18\
    \x06b\0\f\"B\b<\x16^LDFR\x04$N\x1E\\@.&(4J\x060\0>\"\x10\b\n\x16,L\x12F \x04VNP\\\
    \x0E.X(\x02J802>T\x10:\nH,\x1A\x12\x14 6V\x1CP*\x0E`XZ\x02\x188b2\fTB:<H^\x1A\
    D\x14R6$\x1C\x1E*@`&Z4\x18\x06b\0\f\"B\b<\x16^LDFR\x04$N\x1E\\@.&(4J\x060\0>\"\
    \x10\b\n\x16,L\x12F \x04VNP\\\x0E.X(\x02J802>T\x10:\nH,\x1A\x12\x14 6V\x1CP*\x0E\
    `XZ\x02\x188b2\fTB:<H^\x1AD\x14R6$\x1C\x1E*@`&Z4\x18\x06b\0\f\"B\b<\x16^LDFR\x04\
    $N\x1E\\@.&(4J\x060\0>\"\x10\b\n\x16,L\x12F \x04VNP\\\x0E.X(\x02J802>T\x10:\n\
    H,\x1A\x12\x14 6V\x1CP*\x0E`XZ\x02\x188b2\fTB:<H^\x1AD\x14R6$\x1C\x1E*@`&Z4\x18\
    \x06b\0\f\"B\b<\x16^LDFR\x04$N\x1E\\@.&(4J\x060\0>\"\x10\b\n\x16,L\x12F \x04VNP\\\
    \x0E.X(\x02J802>T\x10:\nH,\x1A\x12\x14 6V\x1CP*\x0E`XZ\x02\x188b2\fTB:<H^\x1A\
    D\x14R6$\x1C\x1E*@`&Z4\x18\x06b\0\f\"B\b<\x16^LDFR\x04$N\x1E\\@.&(4J\x060\0>\"\
    \x10\b\n\x16,L\x12F \x04VNP\\\x0E.X(\x02J802>T\x10:\nH,\x1A\x12\x14 6V\x1CP*\x0E\
    `XZ\x02\x188b2\fTB:<H^\x1AD\x14R6$\x1C\x1E*@`&Z4\x18\x06b\0\f\"B\b<\x16^LDFR\x04\
    $N\x1E\\@.&(4J\x060\0>\"\x10\b\n\x16,L\x12F \x04VNP\\\x0E.X(\x02J802>T\x10:\n\
    H,\x1A\x12\x14 6V\x1CP*\x0E`XZ\x02\x188b2\fTB:<H^\x1AD\x14R6$\x1C\x1E*@`&Z4\x18\
    \x06b\0\f\"B\b<\x16^LDFR\x04$N\x1E\\@.&(4J\x060\0>\"\x10\b\n\x16,L\x12F \x04VNP\\\
    \x0E.X(\x02J802>T\x10:\nH,\x1A\x12\x14 6V\x1CP*\x0E`XZ\x02\x188b2\fTB:<H^\x1A\
    D\x14R6$\x1C\x1E*@`&Z4\x18\x06b\0\f\"B\b<\x16^LDFR\x04$N\x1E\\@.&(4J\x060\0>\"\
    \x10\b\n\x16,L\x12F \x04VNP\\\x0E.X(\x02J802>T\x10:\nH,\x1A\x12\x14 6V\x1CP*\x0E\
    `XZ\x02\x188b2\fTB:<H^\x1AD\x14R6$\x1C\x1E*@`&Z4\x18\x06b\0\f\"B\b<\x16^LDFR\x04\
    $N\x1E\\@.&(4J\x060"
- doubleTest: !double "0.4931287132182315"
""")

