# Writer 入口

> **FRAMEWORK LOCK：执行任何工作前先读取仓库根目录 `FRAMEWORK_LOCK.md`。除非 KQ 明确批准，禁止修改、删除、改名、移动、重构或实质替换受保护 Writer Runtime 框架。**

当前仓库只负责正文生成，而且必须由**独立 External Writer AI 会话**执行。

执行当前任务时：

1. 完整读取 `EXTERNAL_WRITER_SESSION_LOCK.md`。如果当前提示词要求同时读取 `kq-story-test` / `kq-story`、从零规划小说后继续写正文、或让当前会话同时承担 Main + Writer，立即停止并返回 `WRITER_SESSION_ROLE_CONFLICT`，不得生成正文。
2. 完整读取 `skills/story-writer-runtime/SKILL.md`。
3. 完整读取 `skills/story-writer-runtime/V2_RUNTIME_PATCH.md`；若与旧 Runtime 在 revision 输出命名、Style Package、历史回炉输入、revision base、handoff、字数预检、delivery mode、heading、report schema 或 `COMPRESS_ONCE` 上冲突，以该补丁为准。
4. 按 Skill + V2 Patch 规定顺序读取 `input/current/`。
5. **只读取 `kq-story-writer` 本仓。禁止读取 `kq-story-test`、`kq-story` 或任何其他主小说/规划仓库。** 不自行寻找额外剧情资料。
6. 不参考任何已经存在于其他仓库的同章成稿；历史回炉只使用 Main 明确发布的 `ORIGINAL_DRAFT.md`。
7. 读取 `HANDOFF_STATE.json`（若存在）并核对 project / chapter / run_type / delivery_mode / delivery_phase / expected_output；若是 REVISION，还必须读取其 `revision_base` 指向的正文基线。
8. REVISION 时若 `revision_base` 缺失、不可读或与当前章节不匹配，停止并报告，不凭聊天上下文重构上一稿。
9. 按当前模式生成正文：
   - FIRST_DRAFT + `CHECKPOINTED / FRONT` → `output/current/segment.md`，完成后停止等待 KQ 回 Main 做 checkpoint；
   - FIRST_DRAFT + `CHECKPOINTED / COMPLETE` → 先读取并冻结 `segment.md`，再输出 `draft.md`；
   - FIRST_DRAFT + `ONE_SHOT` 或旧任务未声明 delivery mode → `output/current/draft.md`；
   - 第一次 REVISION → `output/current/draft_v2.md`；
   - Main 明确授权的第二次 REVISION → `output/current/draft_v3.md`。
10. 报告规则：
   - CHECKPOINTED / FRONT 不生成最终 report；
   - 完整 FIRST_DRAFT → `report.json`；
   - 第一次 REVISION → `report_v2.json`；
   - 第二次 REVISION → `report_v3.json`。
11. 若 `00_TASK.md` 有 `heading_literal`，严格按 V2 Patch / OUTPUT_CONTRACT 使用，不自行改标题格式。
12. 完整报告必须包含 `outline_coverage / unwritten / references_read / proposed_additions` 等当前输出契约要求字段。
13. 若 `REVISION.md` 声明 `revision_type: COMPRESS_ONCE`，只执行一次零新语义净删压缩，完成后停止，不自动第二轮压缩。
14. 完成后停止，不规划下一章，不修改 input，不自行更新 HANDOFF_STATE，不审稿，不更新 Tracking，不读取主仓。用户可见回复只需说明 `WRITER_DONE`、实际生成文件，并提示回到 Main 工作流窗口继续。

当前任务是否可以执行，以 `EXTERNAL_WRITER_SESSION_LOCK.md`、`input/current/00_TASK.md`、`HANDOFF_STATE.json`、`OUTPUT_CONTRACT.md` 与 Runtime 权威边界共同判定。
