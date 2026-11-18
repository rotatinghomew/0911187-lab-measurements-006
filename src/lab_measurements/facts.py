"""实验测量和设备标定记录的身份检查。"""

import json
from pathlib import Path


def load_records(path):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("记录文件必须包含数组")
    records = []
    seen = set()
    for position, record in enumerate(payload):
        if not isinstance(record, dict) or not record.get("id") or record.get("kind") not in {"measurement", "calibration"}:
            raise ValueError(f"第 {position + 1} 条实验记录缺少 id 或 kind")
        if record["id"] in seen:
            raise ValueError(f"重复记录标识：{record['id']}")
        seen.add(record["id"])
        if record["kind"] == "measurement":
            required = ("student_id", "stage", "timepoint", "batch", "calibration_version", "status")
            if any(record.get(field) in (None, "") for field in required):
                raise ValueError(f"测量 {record['id']} 缺少样本、批次或标定信息")
            if record["status"] not in {"valid", "invalid", "revoked"}:
                raise ValueError(f"测量 {record['id']} 的 status 无效")
            value = record.get("value")
            if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float))):
                raise ValueError(f"测量 {record['id']} 的 value 必须是数值或 null")
        elif not all(record.get(field) for field in ("batch", "version", "status")):
            raise ValueError(f"标定 {record['id']} 缺少批次、版本或状态")
        records.append(dict(record))
    return records
