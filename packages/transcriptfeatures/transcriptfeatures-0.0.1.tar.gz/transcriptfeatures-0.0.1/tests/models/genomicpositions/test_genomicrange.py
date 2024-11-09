"""Test GenomicRange class."""

import unittest

from transcriptfeatures.models.genomicpositions.genomicrange import GenomicRange


class GenomicRangeTestCase(unittest.TestCase):
    """Test GenomicRange class."""

    def test_init_succeed(self):
        gr = GenomicRange(ac="AC", start=0, end=0, name="NAME")
        self.assertTrue(isinstance(gr, GenomicRange))

    def test_init_negative_start(self):
        with self.assertRaises(Exception) as context:
            GenomicRange(ac="AC", start=-1, end=0, name="NAME")
        self.assertEqual(
            "start (start position) -1 must be a non-negative integer", str(context.exception)
        )

    def test_init_start_greater_than_end(self):
        with self.assertRaises(Exception) as context:
            GenomicRange(ac="AC", start=1, end=0, name="NAME")
        self.assertEqual(
            "start 1 must be less than or equal to end 0", str(context.exception)
        )
