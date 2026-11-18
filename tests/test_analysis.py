import unittest

from lab_measurements.analysis import summarize
from lab_measurements.reports import build_report


class LabMeasurementTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            {"id": "cal-old", "kind": "calibration", "batch": "b1", "version": "v1", "status": "superseded"},
            {"id": "cal-new", "kind": "calibration", "batch": "b1", "version": "v2", "status": "active"},
            {"id": "m1", "kind": "measurement", "student_id": "s1", "stage": "研一", "timepoint": "t1", "batch": "b1", "calibration_version": "v1", "status": "valid", "value": 10},
            {"id": "m2", "kind": "measurement", "student_id": "s1", "stage": "研一", "timepoint": "t1", "batch": "b1", "calibration_version": "v2", "status": "valid", "value": 8},
            {"id": "m3", "kind": "measurement", "student_id": "s1", "stage": "研二", "timepoint": "t2", "batch": "b1", "calibration_version": "v2", "status": "valid", "value": 6},
            {"id": "m4", "kind": "measurement", "student_id": "s2", "stage": "研一", "timepoint": "t1", "batch": "b1", "calibration_version": "v2", "status": "invalid", "invalid_reason": "仪器漂移", "value": 99},
        ]

    def test_superseded_calibration_and_invalid_reading_do_not_enter_current_mean(self):
        report = build_report(self.records, "lab-r5")
        self.assertEqual(report["analysis"]["stage_batch"]["研一:b1"]["mean"], 8)
        self.assertEqual({row["id"] for row in report["excluded_measurements"]}, {"m1", "m4"})

    def test_repeated_readings_remain_within_student_not_independent_students(self):
        student = summarize(self.records)["repeated_students"]["s1"]
        self.assertEqual(student["reading_count"], 2)
        self.assertEqual(student["within_student_change"], -2)
        self.assertEqual(student["timepoints"], ["t1", "t2"])

    def test_empty_stage_measurement_is_not_reported_as_zero(self):
        self.assertNotIn("研三:b1", summarize(self.records)["stage_batch"])


if __name__ == "__main__":
    unittest.main()
