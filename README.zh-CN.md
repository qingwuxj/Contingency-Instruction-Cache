# 行动分支缓存

[English README](README.md)

行动分支缓存是一种面向动态环境智能体的轻量级设计模式。核心思想是：智能体在执行当前计划的同时，提前生成少量带触发条件的行动分支；当预期状态变化发生时，智能体可以直接切换到缓存分支，而不是从零开始重新完成一次完整决策流程。

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

> agent 能否在继续执行当前步骤时，提前准备少量可能用到的行动分支？

ABC 描述的是下面这个有限的执行模式：

```text
while acting -> precompute action branches -> state changes -> match cached action branch -> validate and switch
```

ABC 使用一个短期 `plan bundle` 保存主线计划和少量 `cached_action_branches`。每个行动分支都包含 `condition`、结构化 `trigger`、结构化 `action`、`valid_if`、过期时间和 fallback。

如果环境变化命中行动分支，系统可以考虑切换到其中的缓存行动；如果缓存失效、变化未知或风险较高，则放弃缓存，进入 `external fallback path` 或请求重新规划。

这个仓库仍然只是一个 idea-first design pattern / schema proposal。它不是新规划算法、完整 agent 框架、实时系统或安全方案，也不声称已经适用于真实机器人或带来经过测量的性能提升。

## Quick Start

```bash
pip install -r requirements.txt
python demo/run_demo.py
python demo/run_demo.py examples/robotic_open_drawer.json
python demo/run_demo.py examples/robotic_pick_cup_bootstrap.json
python -m unittest discover tests -v
```

这个 demo 只回放模拟事件流，不控制机器人或浏览器，不调用 API、不读取办公文件、不发送邮件，也不解析真实 `trigger` 表达式。

## Progressive Branch Hydration

ABC 也可以用 lazy / progressive 方式表达：不一定在第一个动作前就生成完整的 `main_plan + cached_action_branches`。

一种较轻的做法是，agent 先请求一个低风险、可中断、短时有效、需要外部验证的 `bootstrap_action`。在这个 bootstrap action 执行期间，再异步生成后续主线计划和缓存行动分支。

这主要回应一个设计问题：如果一开始就生成全部行动分支，可能增加 first-decision latency。Progressive Branch Hydration 只是可选缓解方式，不表示实时保证，也不绕过 `valid_if`、过期时间、外部验证或 `external fallback path`。

## 这是什么

ABC 是一份轻量的 design note / schema proposal，用来描述一种降低环境变化后 agent decision-to-action latency 的执行组织方式。

它包含：

- 一个 `plan bundle` JSON Schema；
- 几个 embodied-agent、browser-agent 和 office-automation-agent 风格示例；
- 一个最小 demo，用模拟事件流展示缓存命中、缓存失效和重新规划；
- 若干文档，说明它和异步规划、预案规划、行为树、Progressive ABC、plan caching、world models 等概念的关系。

## 这不是什么

ABC 不是：

- 新规划算法；
- 完整 agent 框架；
- 实时机器人系统；
- 安全方案；
- world model；
- perception 或 low-level control 模块。

它只描述一个很窄的问题：如何提前结构化缓存少量可预见的行动分支，从而缩短环境变化后从重新决策到行动切换之间的同步路径。

ABC 关注的不是单纯减少 model waiting time。模型调用可能只是完整决策链的一部分；状态更新、分支形成、行动验证和执行交接也可能产生延迟。

对于办公自动化场景，ABC 也不解决 API 可靠性、文件可用性、用户意图消歧或权限处理。

自然语言描述本身不是可执行 trigger；真实系统需要 monitor adapter 或 detector mapping。ABC 中的 `action` 也必须映射到外部 skill、tool、controller 或 executor 后才可能执行。

## 为什么需要缓存失效条件

缓存行动分支可能过期，也可能因为状态摘要不准确而不再适用。错误缓存会让系统更快做出错误反应。因此 ABC 必须保持短期、少量、可拒绝，并通过 `valid_if`、过期时间和 `replan_if` 明确何时放弃缓存。

ABC 不只用于异常恢复。普通环境变化、状态切换、页面变化、API 状态变化、文件状态变化和用户输入变化，都可以对应行动分支。高风险异常只是其中一种使用场景。

## 示例

仓库中包含三类示例：

- embodied-agent 风格示例：拿杯子、打开抽屉；
- browser-agent 风格示例：填写表单、结账恢复流程；
- office-automation-agent 风格示例：从电子表格准备报告并创建邮件草稿。

这些示例都只是说明 `plan bundle` 和缓存行动分支的表达方式，不表示真实控制能力或安全保证。

## 进一步阅读

- [Concept](docs/concept.md)
- [Architecture](docs/architecture.md)
- [Limitations](docs/limitations.md)
- [Progressive ABC](docs/progressive_abc.md)
- [Related Ideas](docs/related_ideas.md)
- [Scenarios](docs/scenarios.md)
