from mcdu.page import Field

import unittest
from nose.tools import *

class FieldTest(unittest.TestCase):
    def setUp(self):
        self.field = Field("Test", "Test")

    def test_validate_icao(self):
        self.field.format = Field.icao
        self.field.validate("EDDK")
        self.field.validate("ABCD")

    @raises(ValueError)
    def test_validate_icao_1(self):
        self.field.format = Field.icao
        self.field.validate("E1DK")

    @raises(ValueError)
    def test_validate_icao_2(self):
        self.field.format = Field.icao
        self.field.validate("DEF")

    def test_validate_time(self):
        self.field.format = Field.time
        for i in range(0, 24):
            self.field.validate("%02i30Z" % i)
        for i in range(0, 60):
           self.field.validate("12%02iZ" % i)

    @raises(ValueError)
    def test_validate_time_1(self):
        self.field.format = Field.time
        self.field.validate("2415Z")

    @raises(ValueError)
    def test_validate_time_2(self):
        self.field.format = Field.time
        self.field.validate("0560Z")

    @raises(ValueError)
    def test_validate_time_3(self):
        self.field.format = Field.time
        self.field.validate("1130")

    @raises(ValueError)
    def test_validate_time_4(self):
        self.field.format = Field.time
        self.field.validate("425Z")
