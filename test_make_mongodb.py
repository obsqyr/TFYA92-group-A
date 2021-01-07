#!/usr/bin/env python3
import unittest
from make_mongodb import *

# This module tests the script make_mongodb.py

class TestMakeMongodb(unittest.TestCase):
    def test_anynomize_one_symbols(self):
        res = []
        for val in anynomize_one_symbols(["1"]):
            res.append(val)
        self.assertEqual(res, ["A"])

        res = []
        for val in anynomize_one_symbols(["2"]):
            res.append(val)
        self.assertEqual(res, ["A2"])

        res = []
        for val in anynomize_one_symbols(["10", "3", "1"]):
            res.append(val)
        self.assertEqual(res, ["A10", "B3", "C"])

    def test_anynomize_two_symbols(self):
        res = []
        for val in anynomize_two_symbols(["1"]):
            res.append(val)
        self.assertEqual(res, ["Aa"])

        res = []
        for val in anynomize_two_symbols(["2"]):
            res.append(val)
        self.assertEqual(res, ["Aa2"])

        res = []
        for val in anynomize_two_symbols(["10", "3", "1"]):
            res.append(val)
        self.assertEqual(res, ["Aa10", "Ba3", "Ca"])


        string = " 10 1 9 3 "*30 # over 120 numbers
        str_list = string.split()
        res = []
        for value in anynomize_two_symbols(str_list):
            res.append(value)

        expected_res = ['Aa10','Ba','Ca9','Da3','Ea10','Fa','Ga9','Ha3','Ia10',
                        'Ja','Ka9','La3','Ma10','Na','Oa9','Pa3','Qa10','Ra',
                        'Sa9','Ta3','Ua10','Va','Wa9','Xa3','Ya10','Za','Ab9',
                        'Bb3','Cb10','Db','Eb9','Fb3','Gb10','Hb','Ib9','Jb3',
                        'Kb10','Lb','Mb9','Nb3','Ob10','Pb','Qb9','Rb3','Sb10',
                        'Tb','Ub9','Vb3','Wb10','Xb','Yb9','Zb3','Ac10','Bc','Cc9',
                        'Dc3','Ec10','Fc','Gc9', 'Hc3','Ic10','Jc','Kc9','Lc3','Mc10',
                        'Nc','Oc9','Pc3','Qc10','Rc','Sc9','Tc3','Uc10','Vc','Wc9','Xc3',
                        'Yc10','Zc','Ad9','Bd3','Cd10','Dd','Ed9','Fd3','Gd10','Hd',
                        'Id9','Jd3','Kd10','Ld','Md9','Nd3','Od10','Pd','Qd9','Rd3','Sd10',
                        'Td','Ud9','Vd3','Wd10','Xd','Yd9','Zd3','Ae10','Be','Ce9','De3','Ee10',
                        'Fe','Ge9','He3','Ie10','Je','Ke9','Le3','Me10','Ne','Oe9','Pe3']

        self.assertEqual(res, expected_res)

    def test_make_anonymous_form(self):
        res_str = make_anonymous_form("H2O")
        self.assertEqual(res_str, "A2B")

        res_str = make_anonymous_form("Li6Na4")
        self.assertEqual(res_str, "A6B4")

        res_str = make_anonymous_form("Li3Na4Mg")
        self.assertEqual(res_str, "A4B3C")

        # Just hypothetical material of 30 different elements
        string = "Na3Mg5Al"
        res_str = make_anonymous_form(string)
        expected_res = "A5B3C"
        self.assertEqual(res_str, expected_res)

if __name__ == '__main__':
    unittest.main()
