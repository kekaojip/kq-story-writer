# V2_RUNTIME_PATCH.md：Writer Runtime V2 补丁契约

> 本文件是 `skills/story-writer-runtime/SKILL.md` 的增量覆盖层。
>
> 不删除、不重写历史 Runtime；若本文件与 `SKILL.md` 在 revision 输出命名、Style Package、历史回炉输入、handoff、revision base、字数预检、delivery mode、heading、report schema 或 COMPRESS_ONCE 上冲突，以本文件为准。

---

## 1. 启动时额外读取

在 `SKILL.md` 的 00-04 之后，检查并读取当前实际存在的：

```text
05_STYLE_RESOLUTION.md
06_AUTHOR_PREFERENCES.md
ORIGINAL_DRAFT.md
NEXT_CONTEXT.md
REVISION.md
HANDOFF_STATE.json
```

### 权限

- `05_STYLE_RESOLUTION.md`：表达裁决，只控制怎么写。
- `06_AUTHOR_PREFERENCES.md`：当前任务相关 active 作者偏好，只控制表达/已批准设计倾向。
- `ORIGINAL_DRAFT.md`：仅历史章 revision 使用，是待修改原文。
- `NEXT_CONTEXT.md`：仅 revision 时用于后文连续性约束，不是未来剧情设计授权。
- `HANDOFF_STATE.json`：只读交接状态；Writer 不修改 input。

事实权威仍服从原 Runtime：

`04_BOUNDARIES > 01_OUTLINE > 02_CURRENT_STATE > 00_TASK > characters/rules > previous prose > benchmark/execution/style`

表达维度内部：

`00_TASK 当前明确要求 > 05_STYLE_RESOLUTION > 06_AUTHOR_PREFERENCES > benchmark > genre/craft/general references`

Style Package 不得覆盖事实。

---

## 2. 不再跨仓解析文风

Writer 不读取主小说仓，也不自行查询主仓作者记忆。

如果 `references/style-resolution.md` 仍描述单仓时代的：

- 读取主书目录 `设定/文风.md`
- 查询主仓 author-memory
- 回写 `.deslop-whitelist`

在双仓生产任务中，这些步骤由 Main 预编译的 `05_STYLE_RESOLUTION.md / 06_AUTHOR_PREFERENCES.md` 替代。

若任务要求特定风格但 05/06 缺失，且 00_TASK / benchmark 也不足以确定，不猜测，写入 `uncertain_points`；若会实质改变输出方向则阻塞。

---

## 3. FIRST_DRAFT 输出

不存在 `REVISION.md` 时，先看 `delivery_mode / delivery_phase`：

- `ONE_SHOT` 或未声明 delivery mode：`output/current/draft.md + report.json`
- `CHECKPOINTED + FRONT`：只写 `output/current/segment.md`
- `CHECKPOINTED + COMPLETE`：读取已有 `segment.md`，续写完整章，输出 `draft.md + report.json`

详细规则见本文件第 11 节。

保持现有 Human Writing L2 FIRST_DRAFT、execution slices 与只读 preflight 规则。

---

## 4. REVISION 必须先解析基线

存在 `REVISION.md` 时，Writer 必须先读取 `HANDOFF_STATE.revision_base` 指向的正文基线，再执行局部或全文返修。

### 普通第一次返修

典型：

```text
revision_base = output/current/draft.md
```

Writer 必须完整读取该文件，不能只凭 REVISION 摘要、聊天上下文或自己对上一稿的记忆重构原文。

### 普通第二次返修

Main 必须明确指定基线，例如：

```text
revision_base = output/current/draft_v2.md
```

不得自动猜“最新文件”。

### 历史章节回炉

典型：

```text
revision_base = input/current/ORIGINAL_DRAFT.md
```

如果 revision_base 不存在、不可读、章节不匹配或与本轮被审稿版本不一致，停止并申报 `REVISION_BASE_UNRESOLVED`。

---

## 5. REVISION 输出统一为版本化文件

存在 `REVISION.md` 时，**不得覆盖第一稿 `draft.md / report.json`**。

### 第一次返修

若 `HANDOFF_STATE.writer_attempt` 为 2：

```text
output/current/draft_v2.md
output/current/report_v2.json
```

### 第二次返修

只有 Main 明确授权且 `writer_attempt` 为 3：

```text
output/current/draft_v3.md
output/current/report_v3.json
```

默认不允许无限递增。

Writer 在 report 中记录：

```json
{
  "revision_of": "output/current/draft.md",
  "revision_version": 2
}
```

v3 则 `revision_of` 必须与 `HANDOFF_STATE.revision_base` 一致。

---

## 6. 历史章节回炉

若存在 `ORIGINAL_DRAFT.md`：

1. 它必须同时是当前 `revision_base`；
2. `03_PREVIOUS_PROSE.md` 只负责前文衔接，不替代 ORIGINAL_DRAFT；
3. `NEXT_CONTEXT.md` 只用于保护已存在的后文依赖；
4. 不得因为知道后文结果就提前把未来解释写进当前章；
5. 全文重写也必须服从 04_BOUNDARIES 与 REVISION 的 MUST_PRESERVE。

如果历史回炉声明需要原稿而 `ORIGINAL_DRAFT.md` 缺失，停止，不凭主仓不可见内容猜。

---

## 7. Handoff State

读取：

`input/current/HANDOFF_STATE.json`

Writer 只校验：

- project / chapter 是否与 00_TASK 一致；
- run_type 是否与有无 REVISION / ORIGINAL_DRAFT 一致；
- status 是否允许当前执行；
- delivery_mode / delivery_phase 是否与 00_TASK 一致；
- expected_output 是否与本补丁输出命名一致；
- revision 时 `revision_base` 是否存在且可读。

允许 Writer 执行的主要状态：

- `awaiting_external_writer`
- `awaiting_writer_revision`

若状态是 `accepted / archived / blocked`，不得继续写新候选。

Writer 不修改 HANDOFF_STATE；输出完成后由 Main 检测文件并切状态或推进 checkpoint phase。

---

## 8. 字数预检

使用：

```bash
python skills/story-writer-runtime/scripts/measure_draft.py \
  <当前输出正文> \
  --task input/current/00_TASK.md \
  --outline input/current/01_OUTLINE.md
```

解析优先级：

1. `--target` 显式参数
2. `00_TASK.md` 明确用户字数 target / range
3. `01_OUTLINE.md` 标准 `字数目标 + 字数口径`
4. 无法解析 → `target_unresolved`

不得把 `target_unresolved` 报成正常 target check 完成。

用户明确范围优先于自动 ±15% band。

CHECKPOINTED 的 FRONT 不做正式全章 under/over 判定；Main 对 `segment.md` 使用主侧 checkpoint 计算剩余范围。完整 `draft*.md` 才进入最终字数状态。

---

## 9. 输出契约

无论 first draft 或 revision：

- 正文文件只放正文。
- report 放事实申报、deviation、uncertain points、preflight、revision metadata 与本补丁要求的审计字段。
- 不把分析过程写入正文。
- 不为消除 detector flag 自动全文改写。

实际文件名以本文件第 3/5/11 节与 `HANDOFF_STATE.expected_output` 为准。

---

## 10. 热区卫生

Writer 只读取当前任务允许的 `input/current/` 文件，以及：

- CHECKPOINTED + COMPLETE 时当前任务自己的 `output/current/segment.md`；
- revision 时 `revision_base` 明确指向的 Writer 当前输出版本。

如果 Main 已正确发布，目录应只含当前任务材料；Writer 不主动读取 archive，不从上一任务残留“补上下文”。

发现 chapter/project 与 input 文件内部不一致时，停止并申报，不试图自行清理 input。

---

## 11. CHECKPOINTED / ONE_SHOT 第一稿协议

### 11.1 读取字段

Writer 从 `00_TASK.md` 与 `HANDOFF_STATE.json` 读取：

```text
delivery_mode
delivery_phase
heading_literal
checkpoint_actual            # COMPLETE 才有
remaining_user_range         # COMPLETE 才有
front_completed_scope        # COMPLETE 才有
remaining_scope              # COMPLETE 才有
```

若两处声明冲突，停止并报告 `DELIVERY_STATE_CONFLICT`。

未声明 `delivery_mode` 时为向后兼容按 `ONE_SHOT` 执行。

### 11.2 CHECKPOINTED + FRONT

Writer 仍然先读取整章 Outline、Boundaries、Current State、Execution Card 和需要的 references，理解全章后才动笔。

只输出：

`output/current/segment.md`

前段要求：

- 只写已批准内容；
- 在自然场景 / 因果停顿处停，不在一句对白、一个连续动作或必须连写的微场景中间截断；
- 不机械追求 50%；
- 必须给后半保留真实可写的批准内容；
- 不提前写 `remaining_scope` 之后的下一章内容；
- 不输出最终 report；
- 完成后停止，等待 Main checkpoint。

`segment.md` 不是正式候选稿，不得自作主张继续写成整章。

### 11.3 CHECKPOINTED + COMPLETE

必须读取：

`output/current/segment.md`

并把它视为**冻结正文前缀**。

要求：

- segment 原文逐字保留；
- 不为了字数、节奏或“润色”回改 segment；
- 只完成 `remaining_scope` 中尚未落地的批准内容；
- 不重复 `front_completed_scope`；
- checkpoint 的 `remaining_user_range` 只是篇幅反馈，不是新增剧情授权；
- 若剩余空间很紧，优先减少重复解释和无新信息过渡，不得省略必须情节点或把场景改成提纲摘要；
- 最终 `draft.md` 必须由原 segment 原文 + 连续后文组成。

完整 draft 生成后，再执行正常 preflight 并写最终 `report.json`。

### 11.4 ONE_SHOT

直接写完整：

`draft.md + report.json`

不生成 `segment.md`。

Human Writing L2、execution slices、Truth Guard、Review 前置规则均不因 delivery mode 改变。

---

## 12. heading_literal

若 `00_TASK.md` 提供：

`heading_literal: <完整标题首行>`

则 Writer 必须把该 literal **原样**作为正文第一行，不自行改 Markdown 层级、空格、章节号格式或标点。

若：

`heading_literal: NONE`

则正文不加标题行。

CHECKPOINTED 时标题只出现在 `segment.md` 开头；COMPLETE 复用冻结 segment，因此不得在续写部分重复标题。

Revision 默认保持基线标题不变，除非 `REVISION.md` 明确要求改标题。

---

## 13. report.json Final Parity 字段

完整 draft / revision report 在原字段基础上必须增加：

### 13.1 outline_coverage

```json
"outline_coverage": [
  {
    "beat": "批准情节点语义简写",
    "status": "landed|partial|unwritten",
    "location": "正文段落或场景位置"
  }
]
```

要求：

- 覆盖 01_OUTLINE 中本章必须发生的批准情节点；
- `location` 用可复核位置，不写长篇分析；
- Writer 自报 `landed` 不是上游自动 PASS；
- 任何必须情节点 `partial/unwritten` 时，同时写入 `deviations`。

### 13.2 unwritten

```json
"unwritten": [
  {
    "beat": "未成功落地内容",
    "reason": "input_insufficient|boundary_blocked|conflict_or_ambiguity|space_or_pacing|other",
    "note": "最短必要说明"
  }
]
```

只能报告真实没写成的内容，不为了显示“有思考”虚构问题。

`input_insufficient / conflict_or_ambiguity` 不得靠 Writer 自己补世界观或剧情解决。

### 13.3 references_read

```json
"references_read": [
  "skills/human-writing-l2/SKILL.md",
  "skills/story-writer-runtime/references/execution/scene-craft.md"
]
```

只写当前任务**实际读取**的 Skill / reference 路径，不列没读的文件，不把列表长度当质量指标。

### 13.4 proposed_additions 对象化

新报告优先使用：

```json
"proposed_additions": [
  {
    "item": "新增物",
    "type": "character|fact|relation|setting|resource|other",
    "why_needed": "当前场景为什么需要",
    "future_obligation": "none|possible"
  }
]
```

这只是申报，不是授权。

Writer 仍禁止通过 proposed_additions 引入：新主线事件、新反转、新金手指规则、提前后续剧情、改变既定结果。

---

## 14. COMPRESS_ONCE

若 `REVISION.md` 含：

`revision_type: COMPRESS_ONCE`

Writer 将其视为一次专项净删 revision。

必须：

1. 先读取 `HANDOFF_STATE.revision_base`；
2. 保留 heading、全部批准且已落地情节点、事件结果、知识边界、信息释放、伏笔与章尾停点；
3. 不新增任何语义；
4. 只允许删除重复解释、重复反应、无新信息过渡，或合并同义表达；
5. 不改变事件顺序；
6. 不把场景压成摘要 / 提纲；
7. 只执行这一轮，不自动再次 COMPRESS。

完成后按普通版本化 revision 输出，并重新执行受影响 preflight / wordcount。

如果仍然 `over`：

- 在 report 中保留真实结果；
- 停止；
- 不自行继续第二轮压缩。

---

## 15. 接入状态

- style_package: `ENABLED`
- revision_base: `REQUIRED`
- versioned_revision_output: `ENABLED`
- handoff_state: `ENABLED`
- deterministic_wordcount: `TASK_FIRST`
- delivery_mode: `CHECKPOINTED_DEFAULT / ONE_SHOT_SUPPORTED`
- midpoint_checkpoint: `ENABLED`
- heading_literal: `ENABLED`
- report_outline_coverage: `ENABLED`
- report_unwritten_feedback: `ENABLED`
- references_read: `ENABLED`
- proposed_additions_structured: `ENABLED`
- compress_once: `ENABLED`