# 当前输出契约

Writer 完成任务后只新增或更新：

- `draft.md`：完整章节正文。
- `report.json`：新增事实与偏差申报。

`report.json` 最低格式：

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

不得把分析过程、自检说明或下一章规划写入 `draft.md`。
