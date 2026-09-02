# CN WorkDocs

> **把零散材料变成可决策、可追溯、可执行的中文工作文档。**
> Turn scattered evidence into decision-ready Chinese work documents.

[![Validate](https://github.com/zhuyep/cn-workdocs/actions/workflows/validate.yml/badge.svg)](https://github.com/zhuyep/cn-workdocs/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/zhuyep/cn-workdocs)](https://github.com/zhuyep/cn-workdocs/releases)
[![License](https://img.shields.io/github/license/zhuyep/cn-workdocs)](LICENSE)

`cn-workdocs` 是一个面向企业、事业单位、学校、医院、研究机构和项目团队的中文工作文档 Agent Skill，聚焦调研分析、方案计划、工作总结、会议纪要和领导讲话五类场景。它不靠堆砌“高度、力度、深度”，而是控制事实边界、建立证据链、压缩空话，并把判断落实到行动与交付物：少空话、不编造、可核验、能交付。

`cn-workdocs` is an Agent Skill for Chinese enterprise and institutional writing. It helps an AI agent turn incomplete notes and source material into concise, evidence-aware reports, proposals, summaries, meeting minutes, and leadership speeches—without inventing facts or hiding uncertainty behind polished language.

## Why this exists / 为什么做它

普通提示词很容易生成“句句正确、没有一句能负责”的材料：事实与判断混在一起，缺失信息被自动补齐，建议只有方向没有责任人，篇幅很长但无法支持决策。

CN WorkDocs 把写作过程变成一条可检查的流水线：

```text
原始材料 → 事实/推断/建议/未知分层 → 核心判断 → 行动型提纲
        → 正文起草 → 反方审查 → 格式与交付质检
```

This is not another collection of ceremonial templates. It gives the agent an operating method: classify evidence, expose unknowns, write the controlling judgment, structure around the reader's next action, run an adversarial revision, and verify the delivered artifact.

### What it is not / 它不是什么

| Category / 类型 | Primary concern / 主要解决的问题 |
| --- | --- |
| Official-document writer / 公文写作工具 | Statutory document types, formal wording, and administrative relationships / 法定文种、规范措辞与行文关系 |
| Document formatter / 排版工具 | Fonts, margins, headers, page numbers, and a named layout standard / 字体、页边距、版记、页码和指定格式标准 |
| **CN WorkDocs** | Evidence boundaries, decision logic, executable actions, adversarial revision, and delivery QA / 事实边界、决策逻辑、行动落地、反方审查与交付质检 |

CN WorkDocs can work alongside writing and formatting tools, but it deliberately does not pretend to replace their specialized rules.

## What it handles / 适用材料

- 调研报告、分析报告 / research and analysis reports
- 建设方案、实施方案 / proposals and implementation plans
- 工作报告、总结、汇报材料 / work reports and summaries
- 会议纪要 / meeting minutes
- 领导讲话、发言稿 / leadership speeches
- 已有材料的压缩、改写与独立审查 / revision, compression, and independent audit

It is intentionally **not** a legal adviser or a GB/T 9704 formatting guarantee. Mandatory standards require an authoritative template and human verification.

## Four design choices / 四个核心机制

1. **证据控制**：把来源陈述、权威记录、已核事实、推断、建议和未知分开，重要结论必须有依据。
2. **缺口显式化**：缺内容用 `[待补]`，已有但未核验用 `[待核]`，绝不悄悄编造。
3. **行动密度**：把“加强协同、持续推进”还原为责任主体、动作、对象、时间、产出和验收条件。
4. **交付质检**：正文定稿后再做排版，并检查分页、表格、字体替代、引用、时长和隐藏信息。

## Install / 安装

Clone the repository and copy the skill into your agent's skill directory.

克隆仓库，然后把 Skill 复制到智能体的技能目录：

```bash
git clone https://github.com/zhuyep/cn-workdocs.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R cn-workdocs/skills/cn-workdocs "${CODEX_HOME:-$HOME/.codex}/skills/"
```

For project-local use, copy `skills/cn-workdocs` into the skill directory supported by your coding agent. The repository follows the standard `SKILL.md` layout and includes optional Codex interface metadata.

如需项目内共享，可把 `skills/cn-workdocs` 放入所用智能体支持的项目级 Skill 目录。本仓库采用标准 `SKILL.md` 结构，并提供可选的 Codex 界面元数据。

## Try it / 立即试用

```text
Use $cn-workdocs to turn these rough notes into a 1,500-word Chinese
implementation proposal for management. Separate verified facts from
assumptions, mark missing inputs as [待补] and unverified claims as [待核], and end with owners,
milestones, acceptance criteria, risks, and stop conditions.
```

```text
使用 $cn-workdocs，把下面的会议速记整理成正式纪要。严格区分已经形成的决定、
待办事项和仍有分歧的问题；每项任务写清责任人、完成时间和交付物，不要补造共识。
```

## Example / 示例

See [examples/pilot-proposal.md](examples/pilot-proposal.md) for a fictional but realistic example that turns six lines of rough notes into a decision-ready pilot proposal without inventing budget, performance, or policy claims.

查看 [examples/pilot-proposal.md](examples/pilot-proposal.md)：示例将六行零散记录整理为可决策的试点方案，同时把缺失的预算、基线和责任人明确标记为 `[待补]`。

## Repository layout / 仓库结构

```text
skills/cn-workdocs/
├── SKILL.md
├── agents/openai.yaml
└── references/
    ├── evidence-control.md
    ├── document-types.md
    ├── revision-and-tone.md
    └── delivery-and-qa.md
examples/
scripts/validate_repo.py
tests/
```

## Compatibility / 兼容性

The skill is plain Markdown and has no model API dependency. It is designed for Codex and can be adapted to other coding agents that support folder-based Agent Skills. Tool names and installation paths may differ by product.

Skill 本身是纯 Markdown，不调用模型 API。它主要面向 Codex，也可以适配支持目录式 Agent Skill 的其他编程智能体；不同产品的工具名称和安装路径可能不同。

## Contributing / 参与贡献

Real failure cases are more valuable than more slogans. If the skill produces an unsupported claim, vague action, damaged document structure, or unnatural Chinese expression, please open an issue with a sanitized input and the problematic output.

真实失败案例比继续增加口号更有价值。如果 Skill 产生无依据结论、模糊任务、错误文档结构或不自然中文，欢迎提交脱敏后的输入与问题输出。参见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## License / 许可证

[MIT](LICENSE) © Zhuy
