import unittest
from lelei import parser as sp

class TestStructureAutoSizing(unittest.TestCase):

    def test_bitsAreCalculatedCorrectly(self):
        self.assertEqual(sp.bitsForStructure("uint8",  3),  3)
        self.assertEqual(sp.bitsForStructure("uint8",  8),  8)

    def test_uint(self):
        for i in range(1, 32):
            self.assertEqual(sp.bitsForStructure("uint%d"%i, 0), i)
        self.assertEqual(sp.bitsForStructure("uint40", 0), 40)
        self.assertEqual(sp.bitsForStructure("uint48", 0), 48)
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("uint64", 0))

    def test_int(self):
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("int1", 0))
        for i in range(2, 32):
            self.assertEqual(sp.bitsForStructure("int%d"%i, 0), i)
        self.assertEqual(sp.bitsForStructure("int40", 0), 40)
        self.assertEqual(sp.bitsForStructure("int48", 0), 48)

    def test_oversizedTypes(self):
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("uint8", 13))
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("uint16", 17))
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("uint32", 33))
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("uint64", 65))

    def test_negativesizedTypes(self):
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("uint8", -1))
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("uint16", -1))
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("uint32", -1))
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("uint64", -1))

    def test_fieldTypeIsNotDefined(self):
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("float", 0))
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("int", 0))
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("uint", 0))
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("uint128", 0))
        #### this is a possible value! ###
        #self.assertRaises(ValueError, lambda : sp.bitsForStructure("uint3", 0))

class TestFloatSizing(unittest.TestCase):

    def test_floatXX_AutoSizing(self):
        self.assertEqual(sp.bitsForStructure("float32", 0), 32)
        self.assertEqual(sp.bitsForStructure("float32", 0), 32)

    def test_floatXX_sizing(self):
        self.assertEqual(sp.bitsForStructure("float32", 32), 32)
        self.assertEqual(sp.bitsForStructure("float64", 64), 64)

    def test_floatXX_incorrectSizing(self):
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("float32", -1))
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("float32", 16))
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("float32", 33))
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("float64", -1))
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("float64", 33))
        self.assertRaises(ValueError, lambda : sp.bitsForStructure("float64", 65))

