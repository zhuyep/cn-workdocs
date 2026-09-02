# Contributing / 参与贡献

CN WorkDocs values demonstrated improvements over larger instruction files. Please contribute a real, sanitized failure case and the smallest change that fixes it.

CN WorkDocs 更重视经过验证的改进，而不是更长的指令。建议提交真实、脱敏的失败案例，以及能够解决问题的最小修改。

## Good contributions / 推荐贡献

- A sanitized input/output pair showing an unsupported claim, vague action, damaged structure, or unnatural expression.
- A document-type pattern that changes how the agent should reason, not just a list of headings.
- A delivery check that catches a reproducible Word or PDF defect.
- A bilingual documentation correction.

- 能复现无依据结论、模糊任务、结构错误或不自然表达的脱敏案例；
- 真正改变智能体判断方式的文种方法，而不只是标题清单；
- 能稳定发现 Word 或 PDF 交付缺陷的检查规则；
- 中英文文档修正。

## Pull requests / 提交 PR

1. Keep one behavioral change per pull request. / 每个 PR 聚焦一个行为变化。
2. Explain the failure before the fix and why the new rule is narrow enough. / 说明修改前的失败、修改后的效果及规则边界。
3. Do not submit confidential, personal, copyrighted, or organization-specific material without permission. / 不得提交未经授权的机密、个人、受版权保护或单位专属材料。
4. Run the validation suite. / 运行校验：

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

The repository checks YAML/frontmatter, required metadata, local links, and regression tests. Maintainers also run the current platform skill validator before a release.

仓库校验覆盖 YAML/frontmatter、必需元数据、本地链接和回归测试；维护者在发布前还会使用当前平台的 Skill 校验器。

By contributing, you agree that your contribution is licensed under the MIT License.
