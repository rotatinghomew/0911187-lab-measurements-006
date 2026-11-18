"""实验室重复测量记录的身份和数值校验。"""

import json
from pathlib import Path


def load_records(path):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("记录文件必须包含数组")
    records = []
    seen = set()
    for position, record in enumerate(payload):
        required = ("id", "subject", "batch", "method", "replicate")
        if not isinstance(record, dict) or any(record.get(field) in (None, "") for field in required):
            raise ValueError(f"第 {position + 1} 条测量缺少样本或批次字段")
        if record["id"] in seen:
            raise ValueError(f"重复记录标识：{record['id']}")
        seen.add(record["id"])
        value = record.get("value")
        if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float))):
            raise ValueError(f"测量 {record['id']} 的 value 必须是数值或 null")
        records.append(dict(record))
    return records
