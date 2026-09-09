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
  "revision_base": null,
  "expected_output": {
    "draft": "output/current/draft.md",
    "report": "output/current/report.json"
  },
  "note": "optional"
}
```

`revision_base`：

- FIRST_DRAFT：`null`
- 第一次普通返修：`output/current/draft.md`
- 第二次普通返修：Main 明确指定，例如 `output/current/draft_v2.md`
- 历史章回炉：`input/current/ORIGINAL_DRAFT.md`

Writer 在 revision 前必须完整读取该基线。

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

Revision 时 `revision_base` 缺失、不可读或章节不匹配，Writer 必须停止，不得根据聊天上下文猜上一稿。

## Archived 状态持久化

归档完成后，`HANDOFF_STATE.json` 不删除，而是保留为 `status: archived`。

Main 清理热区时可以删除 00-06、REVISION、ORIGINAL_DRAFT、NEXT_CONTEXT、characters/rules/benchmark 和 output 热文件，但必须保留 archived handoff state，直到下一任务发布时被新状态原子替换。

这样新会话可以确定上一章已经真正完成 Tracking + Manifest + 清理，而不是只看到一个空工作区。

状态文件不是小说真相源。事实仍以 Main 发布的 00-04、人物、规则与 Execution Card 权威顺序为准。
