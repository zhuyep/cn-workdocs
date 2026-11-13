# Example: audit unsupported claims / 抓住无依据结论的审查

This fictional example shows Audit mode: it cites the exact draft wording, states the consequence, and gives the smallest safe correction. It does not silently rewrite the document.

本示例完全虚构，用于演示审查模式：逐条引用草稿原句、说明后果，并给出最小安全改法。审查只指出问题，不擅自改写成定稿。

## Draft under review / 送审草稿

```text
# 客服知识助手试运行工作总结（草稿）

本季度客服一次解决率提升 40%，平均响应时间缩短一半。
按公司《知识管理办法（2026）》要求，本月底必须全员上线。
试点部门反馈“很好用”，已证明全面推广条件成熟。
下一步将加强协同、持续推进，尽快形成可复制经验。
```

## Audit findings / 审查发现

本次只做审查，不另出改写稿。

### 1. 无依据业绩（高）

- **原句：** 「本季度客服一次解决率提升 40%，平均响应时间缩短一半。」
- **后果：** 材料里没有口径、基期、样本或来源，把数字写成已核结果，决策者会当成已验收成绩。
- **最小安全改法：** 删除具体升幅，或改为「试点部门反馈一次解决率有改善，升幅与口径均 `[待核]`」；「缩短一半」同样标为 `[待核]`。在补齐基线前，不得把这两项数字当作推广依据。

### 2. 编造政策依据（高）

- **原句：** 「按公司《知识管理办法（2026）》要求，本月底必须全员上线。」
- **后果：** 送审材料中未出现该文件，写成强制依据等于伪造制度，并会把未批准的期限写成必须执行。
- **最小安全改法：** 删去该文件名与「必须」。若确有制度，先补来源再引用；把「本月底全员上线」改为建议，并标 `[待补：依据文件与批准范围]`。

### 3. 将陈述升格为已证事实（中）

- **原句：** 「试点部门反馈“很好用”，已证明全面推广条件成熟。」
- **后果：** 「很好用」只是反馈陈述；「已证明条件成熟」没有给出成功标准或评估记录，不能写成已核结论。
- **最小安全改法：** 保留「试点部门反馈“很好用”」并标明这是陈述；删除「已证明……成熟」，改为「是否推广仍 `[待补：成功标准与评估结论]`」。

### 4. 模糊行动（中）

- **原句：** 「下一步将加强协同、持续推进，尽快形成可复制经验。」
- **后果：** 没有责任人、对象、时间和交付物，无法执行，也无法验收。
- **最小安全改法：** 改成可执行的一句，缺项标 `[待补]`，例如「`[待补：责任人]` 在 `[待补：日期]` 前提交推广或停止建议，并附依据清单」。

## Why this is different / 示例说明

- A reader can see the catch without installing the skill or starting an agent session.
- Audit reports findings first; it does not replace the draft unless the user also asks for a rewrite.
- `[待核]` marks numbers or statements that appeared but are not evidenced; `[待补]` marks missing owners, sources, or criteria.
- 读者不用安装、也不用打开智能体，就能看到空话和假依据会被抓住。
- 审查先给发现，不擅自把草稿改成另一份定稿。
- 已出现但无证据的数字或陈述标 `[待核]`，缺失的责任人、来源或标准标 `[待补]`。
