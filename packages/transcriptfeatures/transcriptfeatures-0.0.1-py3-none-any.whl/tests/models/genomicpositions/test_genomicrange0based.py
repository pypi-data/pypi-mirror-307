"""Test GenomicRange0Based class."""

import unittest

from transcriptfeatures.models.genomicpositions.genomicrange0based import (
    GenomicRange0Based,
)
from transcriptfeatures.models.genomicpositions.sp0based import Sp0Based
from transcriptfeatures.models.genomicpositions.sp1based import Sp1Based


class GenomicRange0BasedTestCase(unittest.TestCase):
    """Test GenomicRange0Based class."""

    def test_init_succeed(self):
        gr0based = GenomicRange0Based(ac="AC", start=0, end=0, name="NAME")
        self.assertTrue(isinstance(gr0based, GenomicRange0Based))

    def test_init_negative_start(self):
        with self.assertRaises(Exception) as context:
            GenomicRange0Based(ac="AC", start=-1, end=0, name="NAME")
        self.assertEqual(
            "start (start position) -1 must be a non-negative integer",
            str(context.exception),
        )

    def test_init_start_greater_than_end(self):
        with self.assertRaises(Exception) as context:
            GenomicRange0Based(ac="AC", start=1, end=0, name="NAME")
        self.assertEqual(
            "start 1 must be less than or equal to end 0", str(context.exception)
        )

    def test_contains_position_is_false(self):
        gr0based = GenomicRange0Based(ac="AC", start=0, end=1, name="NAME")
        self.assertFalse(gr0based.contains_position(0))

    def test_contains_position_is_true(self):
        gr0based = GenomicRange0Based(ac="AC", start=0, end=1, name="NAME")
        self.assertTrue(gr0based.contains_position(1))

    def test_contains_sp0_position_is_false(self):
        ac = "AC"
        gr0based = GenomicRange0Based(ac=ac, start=1, end=2, name="NAME")
        sp0based = Sp0Based(ac=ac, pos=0)
        self.assertFalse(gr0based.contains_sp1_based(sp0based))

    def test_contains_sp0_position_is_true(self):
        ac = "AC"
        gr0based = GenomicRange0Based(ac=ac, start=1, end=2, name="NAME")
        sp0based = Sp0Based(ac=ac, pos=1)
        self.assertTrue(gr0based.contains_sp0_based(sp0based))

    def test_contains_sp1_position_is_false(self):
        ac = "AC"
        gr0based = GenomicRange0Based(ac=ac, start=1, end=2, name="NAME")
        sp1based = Sp1Based(ac=ac, pos=1)
        self.assertFalse(gr0based.contains_sp1_based(sp1based))

    def test_contains_sp1_position_is_true(self):
        ac = "AC"
        gr0based = GenomicRange0Based(ac=ac, start=1, end=2, name="NAME")
        sp1based = Sp1Based(ac=ac, pos=2)
        self.assertTrue(gr0based.contains_sp1_based(sp1based))
