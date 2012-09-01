from mcdu.page import Page

import unittest
from nose.tools import *

class PageTest(unittest.TestCase):
    def setUp(self):
        self.page = Page(None, None)

    def test_validate_icao(self):
        self.page.validate_icao("EDDK")
        self.page.validate_icao("ABCD")

    @raises(ValueError)
    def test_validate_icao_1(self):
        self.page.validate_icao("E1DK")

    @raises(ValueError)
    def test_validate_icao_2(self):
        self.page.validate_icao("DEF")

    def test_validate_time(self):
        for i in range(0, 24):
            self.page.validate_time("%02i30Z" % i)
        for i in range(0, 60):
           self.page.validate_time("12%02iZ" % i)

    @raises(ValueError)
    def test_validate_time_1(self):
        self.page.validate_time("2415Z")

    @raises(ValueError)
    def test_validate_time_2(self):
        self.page.validate_time("0560Z")

    @raises(ValueError)
    def test_validate_time_3(self):
        self.page.validate_time("1130")

    @raises(ValueError)
    def test_validate_time_4(self):
        self.page.validate_time("425Z")
