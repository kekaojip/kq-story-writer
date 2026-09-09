# Writer 入口

> **FRAMEWORK LOCK：执行任何工作前先读取仓库根目录 `FRAMEWORK_LOCK.md`。除非 KQ 明确批准，禁止修改、删除、改名、移动、重构或实质替换受保护 Writer Runtime 框架。**

当前仓库只负责正文生成。

执行当前任务时：

1. 完整读取 `skills/story-writer-runtime/SKILL.md`。
2. 按 Skill 规定顺序读取 `input/current/`。
3. 不读取主小说仓库，不自行寻找额外剧情资料。
4. 不参考任何已经存在于其他仓库的同章成稿。
5. 独立生成正文到 `output/current/draft.md`。
6. 同时生成 `output/current/report.json`。
7. 完成后停止，不规划下一章，不修改 input。

当前任务是否可以执行，以 `input/current/00_TASK.md` 为准。