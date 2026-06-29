# Contingency Instruction Cache

[English README](README.md)

Contingency Instruction Cache（CIC）是一种面向 embodied agents、browser agents 和 office automation agents 的轻量设计模式，讨论如何在环境发生变化时，避免每次都等到事件出现后才首次请求模型重新判断。

它关注的场景包括：

- 机械臂正在伸向杯子，但杯子发生了偏移；
- browser agent 正在填写表单，但弹窗挡住了提交按钮；
- office automation agent 调用 API，但请求失败；
- 任务需要的电子表格缺失或无法读取；
- 用户输入与预期表单值或工作流假设冲突。

这些场景中的等待通常从环境变化后才开始：agent 此时才同步询问模型下一步怎么办。普通流程往往是：

```text
event happens -> ask model -> wait -> decide -> act
```

核心问题是：

> agent 能否在继续执行当前步骤时，提前准备少量可能用到的应对指令？

CIC 描述的是下面这个有限的执行模式：

```text
while acting -> prepare a few likely responses -> event happens -> match cached contingency -> act or replan
```

CIC 使用一个短期 `plan bundle` 保存主线计划和少量 `cached contingency`。每个 cached contingency 都包含 `trigger`、instruction、`valid_if`、过期时间和 fallback。

如果环境变化命中缓存，系统可以先尝试使用缓存中的应对指令；如果缓存失效、事件未知或风险较高，则放弃缓存，进入 `external fallback path` 或请求重新规划。

这个仓库仍然只是一份 design note / schema proposal。它不是新规划算法、完整 agent 框架、实时系统或安全方案，也不声称已经适用于真实机器人或带来经过测量的性能提升。

## Quick Start

```bash
pip install -r requirements.txt
python demo/run_demo.py
python demo/run_demo.py examples/robotic_open_drawer.json
python -m unittest discover tests -v
```

这个 demo 只回放模拟事件流，不控制机器人或浏览器，不调用 API、不读取办公文件、不发送邮件，也不解析真实 `trigger` 表达式。

## 这是什么

CIC 是一份轻量的 design note / schema proposal，用来描述一种降低环境变化后同步决策等待的执行组织方式。

它包含：

- 一个 `plan bundle` JSON Schema；
- 几个 embodied-agent、browser-agent 和 office-automation-agent 风格示例；
- 一个最小 demo，用模拟事件流展示缓存命中、缓存失效和重新规划；
- 若干文档，说明它和异步规划、应急预案、行为树、plan caching、world models 等概念的关系。

## 这不是什么

CIC 不是：

- 新规划算法；
- 完整 agent 框架；
- 实时机器人系统；
- 安全方案；
- world model；
- perception 或 low-level control 模块。

它只描述一个很窄的问题：如何把少量可预见的应对指令提前结构化缓存，从而减少环境变化后的同步等待。

对于办公自动化场景，CIC 也不解决 API 可靠性、文件可用性、用户意图消歧或权限处理。

## 为什么需要缓存失效条件

`cached contingency` 可能过期，也可能因为状态摘要不准确而不再适用。错误缓存会让系统更快做出错误反应。因此 CIC 必须保持短期、少量、可拒绝，并通过 `valid_if`、过期时间和 `replan_if` 明确何时放弃缓存。

## 示例

仓库中包含三类示例：

- embodied-agent 风格示例：拿杯子、打开抽屉；
- browser-agent 风格示例：填写表单、结账恢复流程；
- office-automation-agent 风格示例：从电子表格准备报告并创建邮件草稿。

这些示例都只是说明 `plan bundle` 和 `cached contingency` 的表达方式，不表示真实控制能力或安全保证。

## 进一步阅读

- [Concept](docs/concept.md)
- [Architecture](docs/architecture.md)
- [Limitations](docs/limitations.md)
- [Related Ideas](docs/related_ideas.md)
- [Scenarios](docs/scenarios.md)
