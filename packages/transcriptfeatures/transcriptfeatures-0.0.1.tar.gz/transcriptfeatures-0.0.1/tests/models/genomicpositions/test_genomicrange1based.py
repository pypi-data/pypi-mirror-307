"""Test GenomicRange1Based class."""

import unittest

from transcriptfeatures.models.genomicpositions.genomicrange1based import (
    GenomicRange1Based,
)
from transcriptfeatures.models.genomicpositions.sp0based import Sp0Based
from transcriptfeatures.models.genomicpositions.sp1based import Sp1Based


class GenomicRange1BasedTestCase(unittest.TestCase):
    """Test GenomicRange1Based class."""

    def test_init_succeed(self):
        gr1based = GenomicRange1Based(ac="AC", start=1, end=1, name="NAME")
        self.assertTrue(isinstance(gr1based, GenomicRange1Based))
        
    def test_init_zero(self):
        with self.assertRaises(Exception) as context:
            GenomicRange1Based(ac="AC", start=0, end=0, name="NAME")
        self.assertEqual(
            "start (start position) 0 must be a positive integer",
            str(context.exception),
        )

    def test_init_negative_start(self):
        with self.assertRaises(Exception) as context:
            GenomicRange1Based(ac="AC", start=-1, end=0, name="NAME")
        self.assertEqual(
            "start (start position) -1 must be a positive integer",
            str(context.exception),
        )

    def test_init_start_greater_than_end(self):
        with self.assertRaises(Exception) as context:
            GenomicRange1Based(ac="AC", start=2, end=1, name="NAME")
        self.assertEqual(
            "start 2 must be less than or equal to end 1", str(context.exception)
        )

    def test_contains_position_is_false(self):
        gr1based = GenomicRange1Based(ac="AC", start=2, end=2, name="NAME")
        self.assertFalse(gr1based.contains_position(1))

    def test_contains_position_is_true(self):
        gr1based = GenomicRange1Based(ac="AC", start=2, end=2, name="NAME")
        self.assertTrue(gr1based.contains_position(2))

    def test_contains_sp0_position_is_false(self):
        ac = "AC"
        gr1based = GenomicRange1Based(ac=ac, start=2, end=2, name="NAME")
        sp0based = Sp0Based(ac=ac, pos=0)
        self.assertFalse(gr1based.contains_sp0_based(sp0based))

    def test_contains_sp0_position_is_true(self):
        ac = "AC"
        gr1based = GenomicRange1Based(ac=ac, start=2, end=2, name="NAME")
        sp0based = Sp0Based(ac=ac, pos=1)
        self.assertTrue(gr1based.contains_sp0_based(sp0based))

    def test_contains_sp1_position_is_false(self):
        ac = "AC"
        gr1based = GenomicRange1Based(ac=ac, start=2, end=2, name="NAME")
        sp1based = Sp1Based(ac=ac, pos=1)
        self.assertFalse(gr1based.contains_sp1_based(sp1based))

    def test_contains_sp1_position_is_true(self):
        ac = "AC"
        gr1based = GenomicRange1Based(ac=ac, start=2, end=2, name="NAME")
        sp1based = Sp1Based(ac=ac, pos=2)
        self.assertTrue(gr1based.contains_sp1_based(sp1based))
