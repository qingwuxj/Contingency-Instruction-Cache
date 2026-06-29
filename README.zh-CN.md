# Contingency Instruction Cache

智能体在动态环境中行动时，一类常见等待来自：**环境变化发生后，才第一次同步请求模型判断“怎么办”**。

例如：机器人正在抓杯子，杯子突然偏移；浏览器 agent 正在填写表单，按钮突然不可用。普通流程往往是：

```text
event happens -> ask model -> wait -> decide -> act
```

Contingency Instruction Cache（CIC）讨论一个很小的执行模式：

```text
while acting -> prepare a few likely responses -> event happens -> match cached contingency -> act or replan
```

也就是：智能体在执行当前动作时，提前准备一个短期 `plan bundle`。这个 `plan bundle` 不只包含主线计划，还包含少量可能马上用到的 `cached contingency`：每个 contingency 都有自己的 `trigger`、instruction、`valid_if`、过期时间和 fallback。

如果环境变化命中缓存，系统可以先尝试使用缓存中的应对指令；如果缓存失效、事件未知或风险较高，则放弃缓存，进入 `external fallback path` 或请求重新规划。

CIC 的目标不是让智能体“更聪明”，而是描述如何减少一类常见等待：

> 不要等事件发生后才第一次问“怎么办”。

## 这是什么

CIC 是一份轻量的 design note / schema proposal，用来描述一种降低环境变化后同步决策等待的执行组织方式。

它包含：

- 一个 `plan bundle` JSON Schema；
- 几个 embodied-agent / browser-agent 风格示例；
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

## Quick Start

```bash
pip install -r requirements.txt
python demo/run_demo.py
python demo/run_demo.py examples/robotic_open_drawer.json
python -m unittest discover tests -v
```

这个 demo 只回放模拟事件流，不控制机器人或浏览器，也不解析真实 `trigger` 表达式。

## 为什么需要缓存失效条件

`cached contingency` 可能过期，也可能因为状态摘要不准确而不再适用。错误缓存会让系统更快做出错误反应。因此 CIC 必须保持短期、少量、可拒绝，并通过 `valid_if`、过期时间和 `replan_if` 明确何时放弃缓存。

## 示例

仓库中包含两类示例：

- embodied-agent 风格示例：拿杯子、打开抽屉；
- browser-agent 风格示例：填写表单、结账恢复流程。

这些示例都只是说明 `plan bundle` 和 `cached contingency` 的表达方式，不表示真实控制能力或安全保证。

## 进一步阅读

- [Concept](docs/concept.md)
- [Architecture](docs/architecture.md)
- [Limitations](docs/limitations.md)
- [Related Ideas](docs/related_ideas.md)
- [Scenarios](docs/scenarios.md)
