# Run Modes

Prose Engine 只提供三个正式模式。

它们彼此分开，避免“边写边分析边学习”把上下文搅成一锅。

## 1. WRITE

### 输入

- `PROSE_PACKET`
- 可选 `VOICE_PROFILE`
- 可选召回的 approved anchors

### 任务

生成当前场景正文。

### 读取

- Chinese Prose Base
- Sentence & Paragraph Motion
- Scene Writing
- Character Consciousness
- Dialogue & Handoffs
- Voice System
- Anchor Retrieval
- Prose Generation Loop
- Blind Reader

### 禁止

- 不更新长期 Voice；
- 不分析母本；
- 不把当前 raw draft 加入语料；
- 不设计下一段剧情；
- 不展示内部 Scene Frame。

### 输出

- `draft.md`
- `blind_reader.md`

最终对用户只交正文，除非调用者明确要诊断。

## 2. DISTILL_VOICE

### 输入

- 一个或多个 approved human prose source
- 来源 scope / provenance
- 可选已有 `VOICE_PROFILE`

### 任务

从真人正文或用户认可正文中提取可迁移的声音选择。

### 读取

- Voice Distillation
- Voice System
- VOICE_CORPUS contract
- VOICE_PROFILE contract

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

- `voice_profile.yaml`
- `anchor_index.yaml`
- `confidence_notes.md`

## 3. LEARN_FROM_EDIT

### 输入

- AI before
- 用户/作者 after
- 用户是否明确认可
- 当前 scope
- 可选已有 `VOICE_PROFILE`

### 任务

从真实修改中识别可复用写法差异。

### 读取

- Learning Loop
- Voice System
- VOICE_PROFILE contract

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

这会制造自我污染。

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