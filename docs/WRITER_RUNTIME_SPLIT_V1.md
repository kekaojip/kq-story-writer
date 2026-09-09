# Writer Runtime 拆分清单 V1

源仓库：`kekaojip/kq-story`

目标仓库：`kekaojip/kq-story-writer`

原则：不复制整个 `story-long-write`。主模型保留故事真相、规划、召回选择和状态提交；Writer 只保留正文执行所需规则与确定性质量检查。

## 1. 主模型保留

### Reference

- `author-memory.md`：作者长期偏好权威与查询协议。
- `benchmark-recall.md`：决定本章应该召回哪一本、哪一章、哪种情绪/节奏资产。
- `character-basics.md`
- `character-design-methods.md`
- `character-relations.md`
- `commercial-core-methods.md`
- `cross-book-recall.md`
- `emotional-arc-design.md`
- `emotional-methods.md`
- `fact-correction.md`
- `import-chapter-summary.md`
- `long-outline-template.md`
- `outline-sampling.md`
- `outline-structure-theory.md`
- `project-files.md`
- `reader-contract-and-progression.md`：由主模型负责契约审查，Writer 不重新决定故事兑现。
- `state-tracking.md`
- `suspense-methods.md`：V1 留在规划侧，避免 Writer 擅自重设计悬念。
- `tracking-initialization.md`
- `tracking-transaction.md`
- `workflow-chapter.md`
- `workflow-daily.md`
- `workflow-setup.md`

### Script

- `author_memory_commit.py`
- `build_writer_prompt.py`：保留作为现有上下文编译逻辑参考；后续演化为主仓库侧的 Workspace Publisher。
- `check-outline-contract.js`
- `outline_view.py`
- `storyctl.py`
- `tracking_commit.py`

## 2. Writer Runtime 拆出

### Reference

- `anti-ai-writing.md`
- `banned-words.md`
- `dialogue-mastery.md`
- `long-format.md`
- `writing-craft.md`
- `style-resolution.md`
- `long-chapter-quality.md`：仅作正文自检，不赋予改剧情权限。
- `genre-prose-cards.md` 与 `genre-prose-cards/`：作为正文题材声线库；实际章节由主模型发布当前匹配卡，Writer 不自行改题材。
- `style-genre-modules.md`：无精确题材卡时的正文表达回退。

### Script

- `check-ai-patterns.js`
- `check-degeneration.js`
- `check-outline-copy.js`
- `normalize-punctuation.js`
- `style-whitelist.js`

这些脚本只检查正文形态，不拥有 Tracking 或剧情真相写权限。

## 3. 双方共享，但由主模型决定具体内容

不是把主仓库文件整份同步给 Writer，而是在每章发布时复制最小充分子集：

- 当前章节细纲。
- 当前热状态。
- 上一章真实正文尾部。
- 当前涉及角色的动态状态与必要静态约束。
- 当前涉及的规则/世界约束。
- 已选定的主对标节奏、情绪与文风片段/文件。
- 本章禁止提前释放的信息边界。
- 当前作者偏好的紧凑查询结果。

Writer 只消费这些已选内容，不负责决定召回范围。

## 4. V1 暂不需要

- 原版 `story-long-write/SKILL.md`：职责过宽，不复制；另建瘦身版 `story-writer-runtime/SKILL.md`。
- `artifact-protocols.md`：原版同时承担项目产物协议，V1 的 Writer 输入/输出协议直接写进瘦身 Skill。
- `opening-design.md`：它包含开篇方案选择与重设计能力；V1 由主模型把已经批准的开篇结构发布给 Writer。
- `writer-prompt-fallback.md`：新架构不再 spawn 一段大 prompt，故 V1 不使用。
- `wordcount_core.py`：V1 最终字数裁定仍由主工作流负责；后续需要 Writer 本地预检时再共享。
- `hook-catalog.md`：`reference-index.md` 有引用，但当前 `kq-story/main` 真实树不存在该文件。V1 不补造。

## 5. V1 输入协议

```text
input/current/
├── 00_TASK.md
├── 01_OUTLINE.md
├── 02_CURRENT_STATE.md
├── 03_PREVIOUS_PROSE.md
├── 04_BOUNDARIES.md
├── characters/
├── rules/
└── benchmark/
```

Writer 必须先读取 00-04，再读取当前任务实际提供的子目录文件。不得扫描主仓库，也不得主动读取 `archive/`。

## 6. V1 输出协议

```text
output/current/
├── draft.md
└── report.json
```

`report.json` 至少申报：

- `chapter`
- `status`
- `new_characters`
- `new_facts`
- `uncertain_points`
- `deviations`
- `proposed_additions`

申报不等于事实被接受。只有主模型 PASS 并写回主小说仓库、提交 Tracking 后，新增内容才成为小说真相。

## 7. 审核权限

主模型审核只能做三种裁定：

- `PASS`：接受正文。
- `PASS_WITH_MINOR`：只修名字、标点、明显连续性等机械问题。
- `REWRITE`：生成 `input/current/REVISION.md`，由 Writer 重写。

主模型默认不自己大段润色 Writer 正文，避免重新把成稿改回主模型文风。

## 8. V1 验收

先用《规则维修员》第1章做 A/B：保持剧情、人物、边界和对标不变，只更换正文执行模型。

比较：开头阅读欲、人物活性、对话自然度、场景小说感、偏纲率。

只有外部 Writer 在不偏纲前提下明显优于当前正文，才进入 V2 自动发布/回收和多 Writer 竞赛。
