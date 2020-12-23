#!/usr/bin/env python3

import unittest
from properties import *
import numpy as np
from ase import Atoms
from asap3 import LennardJones


class TestProperties(unittest.TestCase):
    # main functionalities of small functions.
    # Test the infinity - selfdiff first sample
    # Error handling of the system as a whole.

    def test_specific_heat(self):
        temp = [256, 278, 300, 345]
        N = 2
        res = specific_heat(temp, N)
        self.assertAlmostEqual(res, 0.00026289224019185136)

        # test error handling of division with 0
        temp = []
        with self.assertRaises(ValueError) as e:
            specific_heat(temp, N)
        self.assertEqual(str(e.exception), 'temp_store is empty, invalid value.')

    def test_distance2n1(self):
        p1 = [0, 0, 1]
        p2 = [0, 0, 2]
        res1 = distance2(p1, p2)

        p3 = [3, 4, 1]
        p4 = [7, 8, 2]
        p5 = [0, 0, 0]

        res2 = distance2(p3, p4)
        res3 = distance2(p5, p5)
        # Test negative coordinates
        res4 = distance2(-1*np.array(p3), -1*np.array(p4))
        res5 = distance2(p3,p3)
        self.assertEqual(res1, 1)
        self.assertEqual(res2, 4**2+4**2+1)
        self.assertEqual(res3, 0)
        self.assertEqual(res4, res2)
        self.assertEqual(res5, 0) # distance from oneself

        self.assertEqual(distance(p1,p2), res1**(1/2))
        self.assertEqual(distance(p3,p4), res2**(1/2))
        self.assertEqual(distance(p5, p5), res3**(1/2))

    def test_meansquaredisp(self):
        d = 2.9
        L = 10.0
        atoms = Atoms('Au',
                     positions=[[0, L / 2, L / 2]],
                     cell=[d, L, L],
                     pbc=[1, 0, 0])
        res = meansquaredisp(atoms, atoms)
        self.assertEqual(res, 0)

        d = 1.1
        co = Atoms('CO', positions=[(0, 0, 0), (0, 0, d)])
        # test exception handling if number of atoms doesn't match.
        with self.assertRaises(TypeError) as e:
            res = meansquaredisp(co, atoms)
        self.assertEqual(str(e.exception), "Number of atoms doesnt match.")


    def test_energies_and_temp(self):
        d = 2.9
        L = 10.0
        atoms = Atoms('Au',
                     positions=[[0, L / 2, L / 2]],
                     cell=[d, L, L],
                     pbc=[1, 0, 0])
        atoms.calc = LennardJones([18], [0.010323], [3.40], rCut = 6.625, modified = True)

        res = energies_and_temp(atoms)
        self.assertEqual(res, (0, 0, 0, 0))

    def test_lattice_constants(self):
        d = 2.9
        L = 10.0
        atoms = Atoms('Au',
                     positions=[[0, L / 2, L / 2]],
                     cell=[d, L, L],
                     pbc=[1, 0, 0])
        res = lattice_constants(atoms)
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 3)





if __name__ == '__main__':
    unittest.main()
