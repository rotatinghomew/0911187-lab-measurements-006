# 实验室重复测量分析

项目分析不同测量方法在多个实验批次和受试对象上的重复结果。本地合成记录以 `id` 唯一标识，包含 `subject`、`batch`、`method`、`replicate` 和可空的 `value`。

报告将批次内观察分布与对象内成对方法差异分开，列出各自的样本数；不完整配对不会被补成零。当前结果仍按输入文件中的现行数据计算，未保存批次重标或测量更正前的已发布解释。

需要 Python 3.11 或更新版本，无外部服务。执行 `PYTHONPATH=src python -m unittest discover -s tests -v` 运行测试。`lab_measurements.facts` 校验记录，`lab_measurements.pairing.paired_values` 构造对象/批次内完整测量对，`lab_measurements.analysis.summarize` 计算批次及配对指标，`lab_measurements.reports.build_report` 绑定数据修订号。样例见 `examples/sample.json`。
