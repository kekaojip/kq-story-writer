# 双模型小说生产线 V2

## 核心原则

- 主仓库掌握小说真相、规划、Tracking、对标召回、Execution Card 编译和最终验收。
- Writer 仓库只负责当前章节的正文表达。
- Human Writing L2 是 Writer 第一稿行为层，负责避免过度完成，不是后置全文清洗器。
- execution slices 只负责把主模型已批准的悬念、战斗、钩子、反转等意图落成正文。
- `story-review` 留在主仓，负责只读审稿。
- `story-deslop` 留在主仓，生产闭环中只在具体 prose 病灶出现时使用 DETECT_ONLY。
- GitHub 是双方唯一交接层；不依赖聊天上下文保存小说状态。

## V2 每章生命周期

1. Main 读取主仓：细纲、Tracking、相关人物/规则、对标资产、上一章最终正文。
2. Main 完成剧情与执行设计，并按 `writer-execution-card.md` 编译当前章 `EXECUTION_CARD.md`。
3. Main 发布 `input/current/`：
   - `00_TASK.md`
   - `01_OUTLINE.md`
   - `02_CURRENT_STATE.md`
   - `03_PREVIOUS_PROSE.md`
   - `04_BOUNDARIES.md`
   - `characters/`
   - `rules/`
   - `benchmark/`，其中可含 `EXECUTION_CARD.md`
4. Writer 读取 `START_HERE.md` 与 Runtime：
   - FIRST_DRAFT 默认启用 Human Writing L2；
   - 按 `EXECUTION_CARD` 模块加载 execution slices；
   - 生成 `draft.md` 与 `report.json`。
5. Writer 落盘后做只读 deterministic preflight：
   - `check-outline-copy.js`
   - `check-degeneration.js`
   - `measure_draft.py` / `visible_chars_v1`
   - findings 写入 report，不自动全文改写。
6. Main 运行 `story-review` 对 Writer 候选做章节级审查，只输出 findings。
7. 若存在明确 AI / 过度工整 / 解释腔等 prose 病灶，Main 再调用 `story-deslop`：`仅标注 / 只检测 / 不要改`。
8. Main 合并 Writer report、preflight、review findings、必要的 deslop findings 和 Truth/Boundary 判断：
   - PASS：进入收编。
   - PASS WITH MINOR：仅机械级修复。
   - REVISE：创建 `REVISION.md`。
9. Writer 按 `REVISION.md` 局部返修：
   - 自然度问题 → Human Writing L2 LOCAL_REVISION；
   - 真值/连续性/格式问题 → 最小修复；
   - 不借返修重设计剧情。
10. Main 最终 PASS 后把正文写入主仓、裁决 proposed additions、同步 Tracking、归档 Writer manifest。
11. 只有本章正式 PASS + Tracking 同步后，才发布下一章 Workspace。

## Main / Writer / Review 权限

### Main

可以决定：

- 本章发生什么；
- 人物当前知道什么；
- 悬念、反转、爽点、战斗结果与章尾停点；
- 哪些 benchmark / execution module 生效；
- Reviewer finding 是否进入 REVISION；
- Writer 新增细节是否收编；
- Tracking 更新。

### Writer

可以决定：

- 句子怎么写；
- 对话怎么落；
- 已批准事件之间的微连接；
- 当前场景内不产生长期义务的普通细节；
- 已批准 execution intent 如何自然呈现。

禁止：

- 新增主线事件、反转、敌人、奖励、升级、长期伏笔；
- 修改大纲、Tracking、人物真相；
- 为补字数自行加剧情；
- 为清检测器 flag 自动全章人类化。

### Reviewer / Deslop

- `story-review`：只找问题，不改正文。
- `story-deslop`：生产闭环中默认只 DETECT_ONLY；单独用户显式请求去 AI 时仍可按其独立 Skill 原协议运行。
- Main 才拥有最终裁决权。

## Execution Card

Execution Card 是 Main → Writer 的执行意图编译层，不是真相源。

可选模块：

- `PROSE CORE`
- `SUSPENSE`
- `COMBAT`
- `HOOK`
- `REVERSAL`
- `EMOTION`
- `DIALOGUE`

没有的模块不生成。Writer 不得因模块缺失自行补造。

## Writer execution slices

位于：

`skills/story-writer-runtime/references/execution/`

- `scene-craft.md`
- `suspense-execution.md`
- `combat-execution.md`
- `hook-execution.md`
- `reversal-execution.md`

这些都是 execution-only，不拥有规划权。

## 去 AI 分工

```text
FIRST_DRAFT
Human Writing L2
从源头避免过度完成
        ↓
Writer Draft
        ↓
story-review
发现具体正文病灶
        ↓
必要时 story-deslop DETECT_ONLY
进一步定位
        ↓
REVISION.md
        ↓
Writer LOCAL_REVISION
```

默认禁止：

`draft → automatic whole-chapter AI wash → final`

## 回滚

V2 改造前两仓都已建立：

`backup/pre-writer-v2-20260910`

V1 文档与旧 Skill 原件继续保留；V2 不通过真实章节 A/B 时，可回退到该基线。
