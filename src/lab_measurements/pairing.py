"""按实验对象和批次构造完整方法配对。"""

from collections import defaultdict


def paired_values(records, methods):
    by_subject = defaultdict(dict)
    for record in records:
        if record.get("value") is None or record["method"] not in methods:
            continue
        key = (str(record["subject"]), str(record["batch"]))
        by_subject[key].setdefault(str(record["method"]), []).append(float(record["value"]))
    pairs = []
    for (subject, batch), values in sorted(by_subject.items()):
        if all(method in values for method in methods):
            means = {method: sum(values[method]) / len(values[method]) for method in methods}
            pairs.append({"subject": subject, "batch": batch, "values": means})
    return pairs
