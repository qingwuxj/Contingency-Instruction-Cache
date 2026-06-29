# Contingency Instruction Cache

Contingency Instruction Cache（CIC）是一份克制的 design note / schema proposal。它讨论一个很窄的问题：当环境发生变化后，智能体如果每次都同步请求大模型重新规划，会产生等待延迟；CIC 尝试把少量可预见事件的应对指令提前放进一个短期 `plan bundle`，在执行时先尝试匹配缓存。

CIC 不是新算法，不是完整框架，不是实时系统，也不是安全方案。它只描述一种执行组织方式和数据结构，方便开源讨论。

## Quick Start

```bash
pip install -r requirements.txt
python demo/run_demo.py
python demo/run_demo.py examples/robotic_open_drawer.json
python -m unittest discover tests -v
```

这个 demo 只回放模拟事件流，不控制机器人或浏览器，也不解析真实 `trigger` 表达式。

## CIC 关注什么

CIC 关注的是环境变化发生后的同步决策等待。一个普通流程可能是：

```text
event happens -> ask model -> wait -> decide -> act
```

CIC 希望把其中一小部分等待前移：

```text
execute current action -> prepare plan bundle -> event happens -> match cached contingency -> act or replan
```

一个 `plan bundle` 通常包含：

- 一条短期主线计划；
- 少量 `cached contingency`；
- 每个 `cached contingency` 的 `trigger`、instruction、`valid_if`、过期时间和 fallback；
- 若干 `replan_if` 条件，用来说明什么时候不应继续使用缓存。

如果事件匹配缓存且 `valid_if` 仍然成立，执行器可以使用缓存指令。否则，系统应请求重新规划。对于未知或高风险情况，示例中会把流程导向 `external fallback path`，再请求重新规划。

## CIC 不解决什么

CIC 不负责：

- world modeling；
- perception；
- low-level control；
- safety guarantees；
- accurate probability estimation；
- 浏览器或机器人真实执行。

这些能力需要由外部系统提供。CIC 只假设外部系统能提供状态摘要、事件信号、执行接口和自己的风险控制机制。

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
