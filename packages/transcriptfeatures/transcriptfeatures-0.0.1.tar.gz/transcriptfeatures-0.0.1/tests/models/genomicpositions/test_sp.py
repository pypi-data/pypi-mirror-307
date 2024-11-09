"""Test Sp class."""

import unittest

from transcriptfeatures.models.genomicpositions.sp import Sp


class SpTestCase(unittest.TestCase):
    """Test Sp class."""

    def test_init_succeed(self):
        sp = Sp(ac="AC", pos=0)
        self.assertTrue(isinstance(sp, Sp))

    def test_init_negative_pos(self):
        with self.assertRaises(Exception) as context:
            Sp(ac="AC", pos=-1)
        self.assertEqual(
            "pos (position) -1 must be a non-negative integer", str(context.exception)
        )
