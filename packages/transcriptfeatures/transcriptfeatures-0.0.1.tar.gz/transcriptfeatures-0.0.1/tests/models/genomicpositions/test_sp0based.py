"""Test Sp0Based class."""

import unittest

from transcriptfeatures.models.genomicpositions.sp0based import Sp0Based


class Sp0BasedTestCase(unittest.TestCase):
    """Test Sp0Based class."""

    def test_init_succeed(self):
        sp0_based = Sp0Based(ac="AC", pos=0)
        self.assertTrue(isinstance(sp0_based, Sp0Based))

    def test_init_negative_pos(self):
        with self.assertRaises(Exception) as context:
            Sp0Based(ac="AC", pos=-1)
        self.assertEqual(
            "pos (position) -1 must be a non-negative integer", str(context.exception)
        )
