"""选择各设备批次当前有效标定下的有效读数。"""


def current_measurements(records):
    active = {
        str(row["batch"]): str(row["version"])
        for row in records
        if row.get("kind") == "calibration" and row.get("status") == "active"
    }
    return [
        row for row in records
        if row.get("kind") == "measurement"
        and row.get("status") == "valid"
        and row.get("value") is not None
        and active.get(str(row["batch"])) == str(row["calibration_version"])
    ]
