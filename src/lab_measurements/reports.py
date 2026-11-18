"""生成带样本排除原因的重复测量报告。"""

from .analysis import summarize
from .calibration import current_measurements


def build_report(records, source_revision=""):
    if not source_revision:
        raise ValueError("必须提供数据修订标识")
    included = {row["id"] for row in current_measurements(records)}
    return {
        "source_revision": source_revision,
        "record_count": len(records),
        "analysis": summarize(records),
        "excluded_measurements": [
            {"id": row["id"], "status": row.get("status"), "reason": row.get("invalid_reason", "标定版本非当前有效版本或读数缺失")}
            for row in records if row.get("kind") == "measurement" and row["id"] not in included
        ],
    }
