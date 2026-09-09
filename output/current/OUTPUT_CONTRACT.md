# 当前输出契约

Writer 只写 `output/current/`，不修改 input。

## FIRST_DRAFT

不存在 `input/current/REVISION.md` 时：

- `draft.md`：完整章节正文。
- `report.json`：新增事实、偏差与只读预检申报。

## REVISION

存在 `REVISION.md` 时，不覆盖第一稿证据：

- 第一次返修：`draft_v2.md` + `report_v2.json`
- 只有 Main 明确授权第二次返修：`draft_v3.md` + `report_v3.json`

具体 expected output 以 `input/current/HANDOFF_STATE.json.expected_output` 为准，并必须符合 `skills/story-writer-runtime/V2_RUNTIME_PATCH.md`。

Revision 开始前必须读取 `HANDOFF_STATE.revision_base` 指向的正文基线；无法读取时停止。

## Report 最低格式

```json
{
  "chapter": 1,
  "status": "completed",
  "new_characters": [],
  "new_facts": [],
  "uncertain_points": [],
  "deviations": [],
  "proposed_additions": []
}
```

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
