# 双模型小说生产线 V2

## 核心原则

- 主仓库掌握小说真相、规划、Tracking、对标召回、Execution Card 编译、Style Package 编译和最终验收。
- Writer 仓库只负责当前章节的正文表达。
- Human Writing L2 是 Writer 第一稿行为层，负责避免过度完成，不是后置全文清洗器。
- execution slices 只负责把主模型已批准的悬念、战斗、钩子、反转等意图落成正文。
- `story-review` 留在主仓，负责只读审稿。
- `story-deslop` 留在主仓，生产闭环中只在具体 prose 病灶出现时使用 DETECT_ONLY。
- GitHub 是双方唯一交接层；不依赖聊天上下文保存小说状态。
- `HANDOFF_STATE.json` 持久化当前双仓交接阶段；Writer 只读，Main 更新。

## V2 每章生命周期

1. Main 读取主仓：细纲、Tracking、相关人物/规则、对标资产、上一章最终正文。
2. Main 完成剧情与执行设计：
   - 按 `writer-execution-card.md` 编译当前章 `EXECUTION_CARD.md`；
   - 按 `writer-style-package.md` 编译 `05_STYLE_RESOLUTION.md` 与 `06_AUTHOR_PREFERENCES.md`。
3. Main 发布前先清理旧热区并归档需要保留的上一任务证据，然后发布 `input/current/`：
   - `00_TASK.md`
   - `01_OUTLINE.md`
   - `02_CURRENT_STATE.md`
   - `03_PREVIOUS_PROSE.md`
   - `04_BOUNDARIES.md`
   - `05_STYLE_RESOLUTION.md`
   - `06_AUTHOR_PREFERENCES.md`
   - `HANDOFF_STATE.json`
   - `characters/`
   - `rules/`
   - `benchmark/`，其中可含 `EXECUTION_CARD.md`
   - 历史章 revision 时可额外含 `ORIGINAL_DRAFT.md / NEXT_CONTEXT.md / REVISION.md`
4. Writer 读取 `START_HERE.md`、Runtime 与 `V2_RUNTIME_PATCH.md`：
   - FIRST_DRAFT 默认启用 Human Writing L2；
   - 按 `EXECUTION_CARD` 模块加载 execution slices；
   - 按 05/06 执行本次已裁决文风，不跨仓读取主书目录；
   - FIRST_DRAFT 生成 `draft.md` 与 `report.json`；
   - 第一次 REVISION 生成 `draft_v2.md` 与 `report_v2.json`；
   - 第二次 REVISION 只有 Main 明确授权时生成 v3 文件。
5. Writer 落盘后做只读 deterministic preflight：
   - `check-outline-copy.js`
   - `check-degeneration.js`
   - `measure_draft.py --task ... --outline ...` / `visible_chars_v1`
   - findings 写入 report，不自动全文改写；字数目标无法解析时必须报告 `target_unresolved`。
6. Main 把 HANDOFF_STATE 切到 `reviewing`，运行 `story-review` 对 Writer 候选做章节级审查，只输出 findings。
7. 若存在明确 AI / 过度工整 / 解释腔等 prose 病灶，Main 再调用 `story-deslop`：`仅标注 / 只检测 / 不要改`。
8. Main 合并 Writer report、preflight、review findings、必要的 deslop findings 和 Truth/Boundary 判断：
   - PASS：进入收编。
   - PASS WITH MINOR：仅机械级修复。
   - REVISE：创建 `REVISION.md`，更新 HANDOFF_STATE 为 `awaiting_writer_revision`。
9. Writer 按 `REVISION.md` 局部返修：
   - 自然度问题 → Human Writing L2 LOCAL_REVISION；
   - 真值/连续性/格式问题 → 最小修复；
   - 不借返修重设计剧情；
   - 不覆盖第一稿证据，按版本化输出协议生成 v2/v3。
10. Main 最终 PASS 后：
   - 将 HANDOFF_STATE 切到 `accepted`；
   - 把最终采用正文写入主仓；
   - 裁决 proposed additions；
   - 同步 Tracking；
   - 生成 `archive/chapter-{NNN}/MANIFEST.md`；
   - 清理热区；
   - 将 HANDOFF_STATE 切到 `archived`。
11. 只有本章正式 PASS + Tracking 同步 + 归档完成后，才发布下一章 Workspace。

## Main / Writer / Review 权限

### Main

可以决定：

- 本章发生什么；
- 人物当前知道什么；
- 悬念、反转、爽点、战斗结果与章尾停点；
- 哪些 benchmark / execution module 生效；
- 本次文风裁决与 active 作者偏好；
- Reviewer finding 是否进入 REVISION；
- Writer 新增细节是否收编；
- Tracking 更新；
- HANDOFF_STATE 转换与归档完成状态。

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
- 跨仓读取主小说目录；
- 修改 HANDOFF_STATE 或 input；
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

## Style Package

Main 预编译：

- `05_STYLE_RESOLUTION.md`
- `06_AUTHOR_PREFERENCES.md`

Writer 不再使用旧单仓方式自己寻找主书 `设定/文风.md` 或 author-memory。

表达优先级：

`00_TASK 当前明确要求 > 05_STYLE_RESOLUTION > 06_AUTHOR_PREFERENCES > benchmark > genre/craft/general references`

Style Package 只控制表达，不覆盖 00-04 的事实与边界。

## Writer execution slices

位于：

`skills/story-writer-runtime/references/execution/`

- `scene-craft.md`
- `suspense-execution.md`
- `combat-execution.md`
- `hook-execution.md`
- `reversal-execution.md`

这些都是 execution-only，不拥有规划权。

## Revision 输出

```text
FIRST_DRAFT
  draft.md + report.json

REVISION #1
  draft_v2.md + report_v2.json

REVISION #2（仅 Main 明确授权）
  draft_v3.md + report_v3.json
```

Revision 不覆盖第一稿证据；最终收编必须显式记录采用版本。

## 历史章节回炉

历史章 revision 由 Main 额外发布：

- `ORIGINAL_DRAFT.md`
- 必要时 `NEXT_CONTEXT.md`
- `REVISION.md`

Writer 只在这些受控材料范围内修改，不直接读取主仓后文章节。最终 PASS 后 Main 使用现有 `mode=revision` Tracking 协议重算受影响状态。

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

## 热区卫生

发布下一任务前：

1. 先归档需要保留的当前 draft/report/review 证据；
2. `input/current/` 清掉上一任务的 00-06、Revision、Original、Next Context、Handoff、characters/rules/benchmark；
3. `output/current/` 只保留 `OUTPUT_CONTRACT.md`；
4. 再写当前任务。

不得通过“留着也许有用”保留上一章角色、规则或 benchmark。

## Handoff / Archive

- Handoff 协议：`docs/HANDOFF_STATE_CONTRACT.md`
- Archive 模板：`archive/MANIFEST_TEMPLATE.md`

`accepted` 只表示正文已经 PASS；Tracking 与 Manifest 完成并清热区后才进入 `archived`。

## 回滚

V2 第一轮改造前两仓都保留：

`backup/pre-writer-v2-20260910`

第二轮补丁前两仓都保留：

`backup/pre-writer-v2-fix-round2-20260910`

V1 文档与旧 Skill 原件继续保留；如果真实章节 A/B 表现不如预期，可回退到相应基线。
