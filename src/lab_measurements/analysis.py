"""按训练阶段和设备批次分析有效重复测量。"""

from collections import defaultdict

from .calibration import current_measurements


def summarize(records):
    measurements = current_measurements(records)
    groups = defaultdict(list)
    by_student = defaultdict(list)
    for row in measurements:
        groups[(str(row["stage"]), str(row["batch"]))].append(row)
        by_student[str(row["student_id"])].append(row)
    stage_batch = {}
    for (stage, batch), rows in sorted(groups.items()):
        values = [float(row["value"]) for row in rows if row.get("value") is not None]
        stage_batch[f"{stage}:{batch}"] = {
            "students": len({row["student_id"] for row in rows}),
            "readings": len(rows),
            "observed_values": len(values),
            "mean": sum(values) / len(values) if values else None,
            "calibrations": sorted({row["calibration_version"] for row in rows}),
        }
    repeated = {}
    for student, rows in sorted(by_student.items()):
        ordered = sorted(rows, key=lambda row: (row["timepoint"], row["id"]))
        values = [float(row["value"]) for row in ordered if row.get("value") is not None]
        repeated[student] = {
            "timepoints": sorted({row["timepoint"] for row in ordered}),
            "reading_count": len(ordered),
            "within_student_change": values[-1] - values[0] if len(values) >= 2 else None,
            "batches": sorted({row["batch"] for row in ordered}),
        }
    return {"stage_batch": stage_batch, "repeated_students": repeated}
