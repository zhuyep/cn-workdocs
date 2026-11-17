# Example: 60-second self-check after install / 装完 60 秒自检

This page is a post-install check, not a new writing feature. After installing the skill, paste the prompt and notes into a new agent session. In about 60 seconds you should get a minutes draft. The check passes only if all three markers below appear.

本页用于确认 Skill 已生效，不是新的写作功能。安装完成后，把提示词和速记粘贴到新会话。大约 60 秒内应得到一份纪要草稿。下列三项标记都出现才算通过。

## Paste this / 粘贴这一段

```text
使用 $cn-workdocs，把下面的会议速记整理成正式纪要。严格区分已经形成的决定、
待办事项和仍有分歧的问题；每项任务写清责任人、完成时间和交付物，不要补造共识。

- 2026-09-02，客服知识助手讨论会
- 产品：希望 11 月 30 日前上线试用版
- 安全：数据分级前不能把内部资料发给外部模型，部署方案还没同意
- 客服：重复问题大概每天花两小时，没统计过
- 大家同意本周先盘点 50 份代表性文档，不含敏感材料
- 李明说“可以帮忙”，但没说是不是负责人
- 下周二再开会，看数据清单和安全意见
```

## Must appear / 必须出现

| Check / 检查项 | Pass if / 通过条件 | Fail if / 失败条件 |
| --- | --- | --- |
| `[待补]` | 责任人等缺口被显式标出，例如盘点任务的负责人不是“李明” | 把“可以帮忙”写成已确定责任人，或悄悄补上人名 |
| `[待核]` | 未核陈述被标出，例如“每天约两小时”、下次会议的具体日期 | 把估算或“下周二”写成已核事实或已定时间 |
| 已形成的决定 ≠ 建议 | “本周先盘点 50 份代表性文档”写入已形成的决定；“11 月 30 日前上线”不写入已形成的决定 | 把产品方期望写成会议已批准的截止日期 |

## Must not appear / 不得出现

- Treating “李明说可以帮忙” as an accepted owner.
- Treating the unverified “每天约两小时” as a measured fact.
- Converting the product team's wish for a 30 November launch into a meeting decision.
- 把“李明说可以帮忙”写成已接受的负责人。
- 把未经统计的“每天约两小时”写成已核工作量。
- 把产品方“11 月 30 日前上线”的期望写成会议已批准的截止日期。

## Pass / Fail line / 通过或失败一行

Write exactly one of the following after you inspect the draft:

检查草稿后只写下面一行：

- `60s 自检：通过` — all three must-appear checks passed, and none of the must-not-appear failures occurred.
- `60s 自检：失败（缺：…）` — name the missing or violated check.

A complete reference result is in the [meeting minutes example](meeting-minutes.md). Applying this checklist to that published example should read `60s 自检：通过`. A known-bad draft of the same notes is in the [failing minutes example](install-60s-selfcheck-fail.md).

对照完整结果见[会议纪要示例](meeting-minutes.md)。用本清单核对该已发布示例，应得 `60s 自检：通过`。同一组速记的失败对照稿见[失败对照稿](install-60s-selfcheck-fail.md)。

## No-clone check / 免安装核对

You can score the published pass and fail drafts without cloning or starting an agent:

不安装、也不开智能体会话，也可以用下面这条命令核对已发布的通过稿和失败对照稿：

```bash
curl -sL https://raw.githubusercontent.com/zhuyep/cn-workdocs/main/scripts/check_60s_selfcheck.py | python3 - --demo
```

Expected output / 预期输出：

```text
meeting-minutes.md: 60s 自检：通过
install-60s-selfcheck-fail.md: 60s 自检：失败（缺：[待补]；[待核]；已形成的决定 ≠ 建议）
```

If you already have a local draft (including one from a live post-install session), score it with:

若已有本地草稿（包括装完后真实会话的输出），可这样打分：

```bash
python3 scripts/check_60s_selfcheck.py path/to/draft.md
```

This command only scores the published fixture or a file you pass in. It does not replace a live post-install agent session.

该命令只核对已发布示例或你提供的草稿文件，不能代替装完后的真实会话自检。
