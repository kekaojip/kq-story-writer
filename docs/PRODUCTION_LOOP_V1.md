# 双模型小说生产线 V1

## 核心原则

- 主仓库掌握小说真相、规划、Tracking、对标召回和最终验收。
- Writer 仓库只负责当前章节的正文表达。
- GitHub 是双方唯一交接层；不依赖聊天上下文保存小说状态。
- Writer 不得修改主仓库事实，不得自行扩展未来剧情权限。

## 每章固定生命周期

1. 主模型读取主仓库：细纲、Tracking、相关人物/规则、对标资产、上一章正文尾巴。
2. 主模型发布 `input/current/`：
   - `00_TASK.md`
   - `01_OUTLINE.md`
   - `02_CURRENT_STATE.md`
   - `03_PREVIOUS_PROSE.md`
   - `04_BOUNDARIES.md`
   - `characters/`
   - `rules/`
   - `benchmark/`
3. Writer 读取 `START_HERE.md` 和当前工作区，只写：
   - `output/current/draft.md`
   - `output/current/report.json`
4. 主模型审稿：
   - PASS：进入第6步。
   - REWRITE：只新增 `input/current/REVISION.md`，不直接改 Writer 文句。
5. Writer 按 `REVISION.md` 生成：
   - `output/current/draft_v2.md`
   - `output/current/report_v2.json`
   必要时继续 v3，但 V1 默认最多两轮，避免边际收益递减。
6. 主模型验收最终稿，回写主仓库 `正文/第NNN章_*.md`。
7. 主模型同步 Tracking。若最终正文与旧 Tracking 事实不一致，以最终正文为准修正 Tracking，并递增 `state_revision`。
8. Writer 仓库写入 `archive/chapter-NNN/MANIFEST.md`，记录输入/输出 blob、正式收编 commit 和 Tracking commit。Git 历史保留全文版本，不重复复制正文。
9. 清空 `output/current/` 的旧 draft/report，删除旧 `REVISION.md`。
10. 发布下一章 `input/current/`。

## 权限边界

### 主模型可以决定
- 本章发生什么。
- 人物当前知道什么。
- 哪些伏笔推进或禁止释放。
- 世界规则和真相。
- 是否 PASS / REWRITE。
- Writer 新增细节是否收编。

### Writer 可以决定
- 句子怎么写。
- 对话怎么说。
- 动作与段落怎么衔接。
- 场景如何展开。
- 在 `写手自由区` 内增加低等级生活细节。

### Writer 禁止
- 修改大纲、Tracking、主仓库人物真相。
- 新增核心设定、核心人物、独立剧情线。
- 读取 archive 或未来章节，除非当前任务明确授权。
- 把 `proposed_additions` 自动当作长期事实。

## 新增内容申报

Writer 的 `report.json` 应区分：
- `new_characters`：可能需要长期档案的新增角色。
- `proposed_additions`：本章功能位人物、场景名、低等级职业/生活细节。
- `new_facts`：可能改变连续性的事实。
- `uncertain_points`：Writer 不确定、需要主模型裁决的点。
- `deviations`：任何偏离输入契约的行为。

只有主模型验收后的内容才进入主仓库真相。

## V1 质量策略

- 不追求全自动。
- 不让 GPT 直接润色 Writer 正文。
- 审稿只给语义级修订目标，不给成品替换句。
- 一章默认 Writer 初稿 + 最多一次修订。
- 如果第二轮仍只是文风偏好问题，不继续无限打磨，优先积累多章样本后再改 Runtime。
