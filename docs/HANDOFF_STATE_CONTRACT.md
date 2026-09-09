# Handoff State Contract V2

当前双仓任务的交接状态由 Main 写入：

`input/current/HANDOFF_STATE.json`

Writer 只读，不修改 input。

## Schema

```json
{
  "schema": "kq-writer-handoff/v2",
  "project": "书名",
  "chapter": 1,
  "run_type": "create|revision",
  "status": "awaiting_external_writer",
  "writer_attempt": 1,
  "published_at": "ISO-8601",
  "main_source_revision": "optional",
  "writer_repo_base_commit": "optional",
  "expected_output": {
    "draft": "output/current/draft.md",
    "report": "output/current/report.json"
  },
  "note": "optional"
}
```

合法状态：

- `published`
- `awaiting_external_writer`
- `reviewing`
- `awaiting_writer_revision`
- `accepted`
- `archived`
- `blocked`

Writer 只在 `awaiting_external_writer` 或 `awaiting_writer_revision` 时执行。

FIRST_DRAFT 默认输出 `draft.md / report.json`。
第一次 revision 默认输出 `draft_v2.md / report_v2.json`。
第二次 revision 只有 Main 明确授权时使用 `draft_v3.md / report_v3.json`。

状态文件不是小说真相源。事实仍以 Main 发布的 00-04、人物、规则与 Execution Card 权威顺序为准。
