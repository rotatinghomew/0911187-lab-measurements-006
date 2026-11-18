import unittest

from lab_measurements.analysis import summarize
from lab_measurements.reports import build_report


class LabMeasurementTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            {"id": "a1", "subject": "s1", "batch": "b1", "method": "reference", "replicate": 1, "value": 10},
            {"id": "a2", "subject": "s1", "batch": "b1", "method": "candidate", "replicate": 1, "value": 8},
            {"id": "a3", "subject": "s2", "batch": "b1", "method": "reference", "replicate": 1, "value": 20},
            {"id": "a4", "subject": "s2", "batch": "b1", "method": "candidate", "replicate": 1, "value": None},
            {"id": "a5", "subject": "s3", "batch": "b2", "method": "reference", "replicate": 1, "value": 100},
        ]

    def test_pairing_uses_only_subjects_with_both_methods(self):
        result = summarize(self.records)
        self.assertEqual(result["paired_differences"]["candidate-reference"]["paired_subjects"], 1)
        self.assertEqual(result["paired_differences"]["candidate-reference"]["mean_difference"], -2)

    def test_batch_distribution_keeps_unequal_sample_counts_visible(self):
        result = summarize(self.records)
        self.assertEqual(result["batches"]["reference:b1"]["sample_count"], 2)
        self.assertEqual(result["batches"]["reference:b2"]["mean"], 100)

    def test_report_identifies_missing_reading_not_zero(self):
        report = build_report(self.records, "lab-r5")
        self.assertEqual(report["missing_measurements"], ["a4"])
        self.assertEqual(report["source_revision"], "lab-r5")


if __name__ == "__main__":
    unittest.main()
