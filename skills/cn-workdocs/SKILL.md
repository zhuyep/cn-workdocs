---
name: cn-workdocs
description: Draft, revise, compress, or audit evidence-aware Chinese research reports, proposals, work summaries, meeting minutes, and leadership speeches. Use only when one of these five workplace document families or its decision logic fits; do not use for legal conclusions, statutory document selection, or mandatory government formatting without an authoritative template.
---

# CN WorkDocs

Produce Chinese workplace documents that help a reader make a decision or take action. Prefer concrete judgment, traceable evidence, explicit uncertainty, and usable delivery over polished but empty language.

## Route the request

Identify the primary operation before drafting:

- **Draft**: build a document from notes, sources, or a brief.
- **Revise**: preserve the author's meaning while improving logic, specificity, tone, and density.
- **Compress**: shorten without losing decisions, evidence, responsibilities, deadlines, or risks.
- **Audit**: report unsupported claims, logic gaps, vague actions, tone problems, and delivery defects before rewriting.

Then identify the document family. Read [document-types.md](references/document-types.md) for research reports, proposals and plans, work reports, meeting minutes, and leadership speeches. For another genre, use this skill only when one of these five decision structures clearly fits; otherwise state that the request needs a specialist workflow.

If the work relies on claims, figures, policies, named organizations, quotations, or current information, read [evidence-control.md](references/evidence-control.md). For Audit, Revise, or Compress, also read [revision-and-tone.md](references/revision-and-tone.md). If the requested output is Word or another formatted artifact, read [delivery-and-qa.md](references/delivery-and-qa.md).

## Working method

1. **Read the assignment as a decision problem.** Establish the audience, purpose, decision or action expected, source boundary, tone, length, deadline, and delivery format. If details are missing, continue with conservative assumptions and mark material gaps as `[待补]`; mark supplied but unverified statements as `[待核]`.
2. **Inventory the material.** Separate supplied statements, authoritative records, verified facts, inferences, opinions, requests, and unknowns. Never promote a statement or inference into a verified fact.
3. **Write the controlling judgment.** Before expanding sections, state in one or two sentences what the reader should conclude and why. If the evidence does not support a conclusion, say so.
4. **Design the outline around the reader's next action.** Use a problem–evidence–judgment–action chain. Do not default to a ceremonial outline when the task needs a decision.
5. **Draft with information density.** Each paragraph should perform one job. Replace slogans with actors, actions, objects, timing, conditions, evidence, or measurable outcomes when the material supports them.
6. **Run an adversarial revision.** Test whether a skeptical reader can distinguish fact from interpretation, identify the basis for important claims, understand tradeoffs, and know what happens next.
7. **Deliver the requested artifact.** Keep drafting notes and source ledgers out of the main body unless the user requests them, but preserve a concise assumptions or verification list when unresolved points affect correctness.

## Non-negotiable rules

- Do not invent figures, policies, quotations, source titles, people, organizational positions, achievements, or deadlines.
- Use `[待补]` for missing content the author must supply and `[待核]` for content that exists but requires verification. Do not use placeholders to hide avoidable research.
- Keep facts, inferences, recommendations, and rhetoric distinguishable through wording and structure.
- Preserve authoritative wording, approved numbers, and assigned responsibilities during revision unless the user explicitly authorizes substantive change.
- Avoid inflated political, strategic, or management language that adds no decision value. Necessary institutional language should frame the argument, not replace it.
- Do not claim compliance with GB/T 9704 or another mandatory standard unless an authoritative template or standard is available and the output has been checked against it.
- For legal, policy, financial, safety, personnel, or public-release material, surface the need for qualified human review.

## Default output contract

For Draft, Revise, and Compress, return:

1. the finished document body;
2. a short `信息缺口与核验事项` section only when unresolved items materially affect the result;
3. a short `依据与边界` section when external sources or important assumptions were used, with enough source locators to reproduce important claims.

For Audit, return prioritized findings, the exact passage or evidence behind each finding, its consequence, and the smallest safe correction. Do not silently rewrite the document unless the user also asks for a revised version.

Do not expose chain-of-thought or produce a long process diary. Give the reader the result and the evidence needed to trust or revise it.
