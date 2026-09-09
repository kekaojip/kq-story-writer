# V2_RUNTIME_PATCH.md：Writer Runtime V2 补丁契约

> 本文件是 `skills/story-writer-runtime/SKILL.md` 的增量覆盖层。
>
> 不删除、不重写历史 Runtime；若本文件与 `SKILL.md` 在 revision 输出命名、Style Package、历史回炉输入、handoff 或字数预检上冲突，以本文件为准。

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

不存在 `REVISION.md` 时：

```text
output/current/draft.md
output/current/report.json
```

保持现有 Human Writing L2 FIRST_DRAFT、execution slices 与只读 preflight 规则。

---

## 4. REVISION 输出统一为版本化文件

存在 `REVISION.md` 时，**不得覆盖第一稿 `draft.md / report.json`**。

### 第一次返修

若 `HANDOFF_STATE.writer_attempt` 为 2，或当前只有第一稿：

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
  "revision_of": "draft.md",
  "revision_version": 2
}
```

v3 则 `revision_of` 指向上一个被 Main 选作返修基线的版本。

---

## 5. 历史章节回炉

若存在 `ORIGINAL_DRAFT.md`：

1. 它是当前 revision 的正文基线；
2. `03_PREVIOUS_PROSE.md` 只负责前文衔接，不替代 ORIGINAL_DRAFT；
3. `NEXT_CONTEXT.md` 只用于保护已存在的后文依赖；
4. 不得因为知道后文结果就提前把未来解释写进当前章；
5. 全文重写也必须服从 04_BOUNDARIES 与 REVISION 的 MUST_PRESERVE。

如果 `REVISION.md` 存在但历史回炉任务声明需要原稿，而 `ORIGINAL_DRAFT.md` 缺失，停止，不凭主仓不可见内容猜。

---

## 6. Handoff State

读取：

`input/current/HANDOFF_STATE.json`

Writer 只校验：

- project / chapter 是否与 00_TASK 一致；
- run_type 是否与有无 REVISION / ORIGINAL_DRAFT 一致；
- status 是否允许当前执行；
- expected_output 是否与本补丁输出命名一致。

允许 Writer 执行的主要状态：

- `awaiting_external_writer`
- `awaiting_writer_revision`

若状态是 `accepted / archived / blocked`，不得继续写新候选。

Writer 不修改 HANDOFF_STATE；输出完成后由 Main 检测文件并切到 reviewing。

---

## 7. 字数预检

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

---

## 8. 输出契约

无论 first draft 或 revision：

- 正文文件只放正文。
- report 放事实申报、deviation、uncertain points、preflight、revision metadata。
- 不把分析过程写入正文。
- 不为消除 detector flag 自动全文改写。

实际文件名以本文件第 3/4 节与 `HANDOFF_STATE.expected_output` 为准。

---

## 9. 热区卫生

Writer 只读取当前 `input/current/` 实际存在文件。

如果 Main 已正确发布，目录应只含当前任务材料；Writer 不主动读取 archive，不从上一任务残留“补上下文”。

发现 chapter/project 与 input 文件内部不一致时，停止并申报，不试图自行清理 input。
