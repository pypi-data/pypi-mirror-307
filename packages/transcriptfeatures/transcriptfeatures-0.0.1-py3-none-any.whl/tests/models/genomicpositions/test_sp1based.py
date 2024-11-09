"""Test Sp1Based class."""

import unittest

from transcriptfeatures.models.genomicpositions.sp1based import Sp1Based


class Sp1BasedTestCase(unittest.TestCase):
    """Test Sp1Based class."""

    def test_init_succeed(self):
        sp1_based = Sp1Based(ac="AC", pos=1)
        self.assertTrue(isinstance(sp1_based, Sp1Based))

    def test_init_zero(self):
        with self.assertRaises(Exception) as context:
            Sp1Based(ac="AC", pos=0)
        self.assertEqual(
            "pos (position) 0 must be a positive integer", str(context.exception)
        )

    def test_init_negative_pos(self):
        with self.assertRaises(Exception) as context:
            Sp1Based(ac="AC", pos=-1)
        self.assertEqual(
            "pos (position) -1 must be a positive integer", str(context.exception)
        )
