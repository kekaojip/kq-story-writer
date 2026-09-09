# kq-story-writer

外部正文模型专用运行仓库。

## 定位

本仓库不是小说真相库，也不是规划仓库。它只负责消费主工作流发布的当前章节工作区，并生成正文候选稿。

- 主工作流决定：写什么、谁知道什么、哪些事实成立、哪些信息禁止提前释放。
- Writer 决定：这些已批准内容如何变成自然、可读的小说正文。
- Human Writing L2 决定：第一稿如何避免过度完成、过度解释和统一化的“满分答案”质感。
- Execution Card / execution slices：把主模型已批准的悬念、战斗、钩子、反转等执行意图传给 Writer，但不授予剧情设计权。
- GitHub 负责：跨模型交接、版本、审计和持久化。

## 权限边界

Writer 可以：

- 读取 `input/current/` 当前任务。
- 读取本仓库的 `skills/story-writer-runtime/` 与 `skills/human-writing-l2/`。
- 在 `output/current/` 写正文草稿与申报报告。
- 对现场微小连接、普通措辞、非长期场景细节做创作选择。

Writer 不可以：

- 修改主小说仓库。
- 修改全书大纲、卷纲、细纲、Tracking、角色权威设定或世界真相。
- 自行新增会影响后续的能力、组织、人物关系、长期伏笔或世界规则。
- 因为知道某个未来规划而提前泄露它。
- 为补字数、清检测器 flag 或“更刺激”而新增剧情。

## V2 工作流

`主模型规划 → 编译 EXECUTION_CARD → 发布 input/current → Writer + Human Writing L2 + execution slices → draft/report → deterministic preflight → 主仓 story-review → 必要时 story-deslop DETECT_ONLY → Main PASS / REVISION → Writer LOCAL_REVISION → 正式入主小说仓库 + Tracking`

详细协议见：

- `docs/PRODUCTION_LOOP_V2.md`
- `skills/story-writer-runtime/SKILL.md`

V1 历史协议继续保留在 `docs/PRODUCTION_LOOP_V1.md` 与 `docs/WRITER_RUNTIME_SPLIT_V1.md`，不覆盖、不删除。

V2 改造前基线：`backup/pre-writer-v2-20260910`。
