# 实验室重复测量分析

项目分析研究生不同训练阶段的重复测量，保留学生、测量时点、设备批次、标定版本和读数有效状态。本地合成 JSON 中 `calibration` 记录标记批次当前有效的设备标定，`measurement` 记录标注 `valid`、`invalid` 或 `revoked`。

当前统计只使用有效标定下且有数值的测量，分别报告阶段/批次构成和学生自身跨时点变化；无有效读数的阶段不会伪造零值。被排除的读数仍在报告中带出原因。项目当前使用输入中标记为 active 的标定，尚未保留组会结论使用过的标定版本及受后续校准影响的结论。

需要 Python 3.11 或更新版本，无外部服务。执行 `PYTHONPATH=src python -m unittest discover -s tests -v` 运行测试。`lab_measurements.facts` 校验测量/标定身份，`lab_measurements.calibration.current_measurements` 选择当前有效读数，`lab_measurements.analysis.summarize` 分析批次样本和个体重复测量，`lab_measurements.reports.build_report` 列出排除原因并绑定数据修订。样例见 `examples/sample.json`。
