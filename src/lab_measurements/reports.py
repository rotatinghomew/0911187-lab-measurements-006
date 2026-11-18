"""生成可追溯的实验批次分析。"""

from .analysis import summarize


def build_report(records, source_revision=""):
    if not source_revision:
        raise ValueError("必须提供数据修订标识")
    return {
        "source_revision": source_revision,
        "record_count": len(records),
        "analysis": summarize(records),
        "missing_measurements": [record["id"] for record in records if record.get("value") is None],
    }
