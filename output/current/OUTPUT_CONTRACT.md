# 当前输出契约

Writer 只写 `output/current/`，不修改 input。

## FIRST_DRAFT

不存在 `input/current/REVISION.md` 时，先看 `delivery_mode / delivery_phase`。

### ONE_SHOT

- `draft.md`：完整章节正文。
- `report.json`：新增事实、偏差、覆盖情况与只读预检申报。

### CHECKPOINTED / FRONT

- `segment.md`：当前章前段正文，只用于 midpoint checkpoint。
- 不生成最终 `report.json`。
- `segment.md` 不是正式候选稿，不得进入 Review、Tracking 或正式收编。

### CHECKPOINTED / COMPLETE

- 必须先读取现有 `segment.md`。
- `segment.md` 作为冻结正文前缀，原文不得回改。
- `draft.md`：`segment.md` 原文 + 后续剩余批准内容。
- `report.json`：完整章最终报告。

具体 expected output 以 `input/current/HANDOFF_STATE.json.expected_output` 为准，并必须符合 `skills/story-writer-runtime/V2_RUNTIME_PATCH.md`。

## REVISION

存在 `REVISION.md` 时，不覆盖第一稿证据：

- 第一次返修：`draft_v2.md` + `report_v2.json`
- 只有 Main 明确授权第二次返修：`draft_v3.md` + `report_v3.json`

Revision 开始前必须读取 `HANDOFF_STATE.revision_base` 指向的正文基线；无法读取时停止。

若 `revision_type: COMPRESS_ONCE`，仍使用同一版本化输出规则；只能执行一次净删压缩，不得新增语义或自动继续第二轮压缩。

## heading_literal

若 `00_TASK.md` 提供完整 `heading_literal`：

- 原样写作正文第一行；
- 不改变 Markdown 层级、空格、章节号样式或标点；
- CHECKPOINTED 时只在 `segment.md` 开头出现一次；
- COMPLETE 阶段不得重复标题；
- Revision 默认保持基线标题不变。

若 `heading_literal: NONE`，正文不加标题行。

## Report 最低格式

完整 draft / revision 的报告最低格式：

```json
{
  "chapter": 1,
  "status": "completed",
  "new_characters": [],
  "new_facts": [],
  "uncertain_points": [],
  "deviations": [],
  "outline_coverage": [],
  "unwritten": [],
  "references_read": [],
  "proposed_additions": []
}
```

### outline_coverage

```json
"outline_coverage": [
  {
    "beat": "批准情节点语义简写",
    "status": "landed|partial|unwritten",
    "location": "正文段落或场景位置"
  }
]
```

必须覆盖本章批准的必发生情节点。任何必须情节点为 `partial / unwritten` 时，同时写入 `deviations`。

### unwritten

```json
"unwritten": [
  {
    "beat": "未成功落地内容",
    "reason": "input_insufficient|boundary_blocked|conflict_or_ambiguity|space_or_pacing|other",
    "note": "最短必要说明"
  }
]
```

只报告真实没写成的内容，不自行补剧情解决输入缺口。

### references_read

```json
"references_read": [
  "skills/human-writing-l2/SKILL.md",
  "skills/story-writer-runtime/references/execution/scene-craft.md"
]
```

只列当前任务实际读取的 Skill / reference 路径。

### proposed_additions

新报告优先使用对象：

```json
"proposed_additions": [
  {
    "item": "新增物",
    "type": "character|fact|relation|setting|resource|other",
    "why_needed": "当前场景为什么需要",
    "future_obligation": "none|possible"
  }
]
```

这只是申报，不扩大 Writer 的新增权限。

Revision report 额外记录，并与 HANDOFF_STATE 保持一致：

```json
{
  "revision_of": "output/current/draft.md",
  "revision_version": 2
}
```

允许附：

- `preflight.outline_copy`
- `preflight.degeneration`
- `preflight.wordcount`

不得把分析过程、自检说明、Reviewer 报告或下一章规划写入正文文件。
不得为了清 detector flag 自动全文改写。