# Run Modes

Prose Engine 只提供三个正式模式。

它们彼此分开，避免“边写边分析边学习”把上下文搅在一起。

## 1. WRITE

### 输入

- `PROSE_PACKET`
- 可选长期 Voice 数据
- 可选 previous accepted prose tail

### 编译

先由 `architecture/CONTEXT_COMPILER.md` 生成：

- `WRITER_CONTEXT`
- `ACTIVE_VOICE_CONTEXT`（可空）

Writer 不直接读取完整 Voice Profile、整本母本或完整大纲。

### 第一稿读取

默认只读：

1. `WRITER_CONTEXT`
2. `runtime/WRITE_CORE.md`
3. `ACTIVE_VOICE_CONTEXT`（存在时）
4. 必要 previous prose tail

**不默认读取全部 references。**

只有出现明确病灶时，才按 `SKILL.md` progressive disclosure 路由一个对应 reference。

### 第一稿任务

只生成当前场景正文。

第一稿不同时扮演 Reviewer，不边写边评分，也不更新 Voice。

### Blind Reader

正文完成后独立运行：

- `runtime/BLIND_READER_CORE.md`
- 当前正文
- 一句目标读者

Blind Reader 不看到 PROSE_PACKET、Voice、作者意图。

### Repair

只有 Blind Reader 出现真实 finding 时：

1. 编译 `REPAIR_PACKET`
2. 读取 `runtime/LOCAL_REPAIR_CORE.md`
3. 执行一次局部返修

没有 finding 就直接接受当前正文层结果。

### 禁止

- 不更新长期 Voice；
- 不分析母本；
- 不把当前 raw draft 加入语料；
- 不设计下一段剧情；
- 不展示内部 Context Compiler 产物；
- 不全文 humanize；
- 不进行多轮 Judge 优化。

### 输出

运行内部可以存在：

- draft
- blind reader findings
- repair packet
- repaired draft

对外默认只交最终正文，除非调用者明确要求诊断。

## 2. DISTILL_VOICE

### 输入

- 一个或多个 approved human prose source
- 来源 scope / provenance
- 可选已有 `VOICE_PROFILE`

### 任务

从真人正文或用户认可正文中提取可迁移的声音选择。

### 读取

- `references/voice-distillation.md`
- `references/voice-system.md`
- `references/voice-validation.md`
- `specs/VOICE_CORPUS.md`
- `specs/VOICE_PROFILE.md`

### 方法

默认使用：

`Human Sample → Semantic Skeleton → Neutral Baseline → Contrast → Claim+Evidence → Cross-sample clustering → Scope filter`

### 禁止

- 不写小说新正文；
- 不把剧情内容当文风；
- 不从 raw AI draft 蒸馏正向 Voice；
- 不把单个漂亮句升级为作者原则；
- 不输出硬生成配额。

### 输出

- Voice Profile
- Anchor Index
- confidence notes

## 3. LEARN_FROM_EDIT

### 输入

- AI before
- 用户/作者 approved after
- 当前 scope
- 可选已有 `VOICE_PROFILE`

### 任务

从真实修改中识别可复用写法差异。

### 读取

- `references/learning-loop.md`
- `references/voice-system.md`
- `specs/VOICE_PROFILE.md`

### 方法

先过滤：

- 标点；
- 错别字；
- 专名；
- 单次剧情事实。

再提取：

- 叙事距离变化；
- 搭配变化；
- 解释删除；
- 对白接法；
- 段落切法；
- 心理处理；
- 抽象 → 具体 / 人物词汇变化。

### 输出

默认只生成候选：

```yaml
voice_update_proposals:
  - trait: ""
    dimension: ""
    evidence: ""
    scope: ""
    confidence: low|medium|high
```

没有足够证据时不更新正式 Profile。

## 模式隔离原则

一次运行只允许一个主模式。

特别禁止：

`WRITE → AI 自己评价不错 → 自动 LEARN → 把自己的稿当 Voice`

允许的闭环是：

`WRITE → 人类接受/修改 → 下一次单独 LEARN_FROM_EDIT`

或者：

`真人母本 → DISTILL_VOICE → WRITE`

## 为什么只有三个模式

正文模块越能做所有事，越容易重新变成总工作流。

本模块只围绕“文字本身”保留：

- 写；
- 学声音；
- 从真实修改变准。

剧情、设定、商业分析、章节规划、Tracking 都属于模块之外。
