# Writer 入口

> **FRAMEWORK LOCK：执行任何工作前先读取仓库根目录 `FRAMEWORK_LOCK.md`。除非 KQ 明确批准，禁止修改、删除、改名、移动、重构或实质替换受保护 Writer Runtime 框架。**

当前仓库只负责正文生成。

执行当前任务时：

1. 完整读取 `skills/story-writer-runtime/SKILL.md`。
2. 完整读取 `skills/story-writer-runtime/V2_RUNTIME_PATCH.md`；若与旧 Runtime 在 revision 输出命名、Style Package、历史回炉输入、revision base、handoff 或字数预检上冲突，以该补丁为准。
3. 按 Skill + V2 Patch 规定顺序读取 `input/current/`。
4. 不读取主小说仓库，不自行寻找额外剧情资料。
5. 不参考任何已经存在于其他仓库的同章成稿；历史回炉只使用 Main 明确发布的 `ORIGINAL_DRAFT.md`。
6. 读取 `HANDOFF_STATE.json`（若存在）并核对 project / chapter / run_type / expected_output；若是 REVISION，还必须读取其 `revision_base` 指向的正文基线。
7. REVISION 时若 `revision_base` 缺失、不可读或与当前章节不匹配，停止并报告，不凭聊天上下文重构上一稿。
8. 按当前模式生成正文：
   - FIRST_DRAFT → `output/current/draft.md`
   - 第一次 REVISION → `output/current/draft_v2.md`
   - Main 明确授权的第二次 REVISION → `output/current/draft_v3.md`
9. 同步生成对应报告：`report.json / report_v2.json / report_v3.json`。
10. 完成后停止，不规划下一章，不修改 input，不自行更新 HANDOFF_STATE。

当前任务是否可以执行，以 `input/current/00_TASK.md`、`HANDOFF_STATE.json` 与 Runtime 权威边界共同判定。
