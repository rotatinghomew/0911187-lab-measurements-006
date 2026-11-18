"""分开呈现实验批次分布与受试对象内的配对差异。"""

from collections import defaultdict
from .pairing import paired_values


def summarize(records):
    batches = defaultdict(list)
    for record in records:
        key = (str(record["method"]), str(record["batch"]))
        batches[key].append(record)
    batch_results = {}
    for (method, batch), rows in sorted(batches.items()):
        values = [float(row["value"]) for row in rows if row.get("value") is not None]
        batch_results[f"{method}:{batch}"] = {
            "sample_count": len(rows),
            "observed_count": len(values),
            "mean": sum(values) / len(values) if values else None,
            "minimum": min(values) if values else None,
            "maximum": max(values) if values else None,
        }
    methods = sorted({str(row["method"]) for row in records})
    differences = defaultdict(list)
    if len(methods) >= 2:
        for pair in paired_values(records, methods[:2]):
            values = pair["values"]
            differences[f"{methods[0]}-{methods[1]}"].append(values[methods[0]] - values[methods[1]])
    paired_results = {
        key: {"paired_subjects": len(values), "mean_difference": sum(values) / len(values) if values else None}
        for key, values in sorted(differences.items())
    }
    return {"batches": batch_results, "paired_differences": paired_results}
