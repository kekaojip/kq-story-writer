# Standalone Prose Engine V1

这是一个**完全独立的中文小说正文生成模块设计**。

当前只存在于：

```text
branch: design/prose-engine-v1
path: standalone/prose-engine-v1/
```

它没有接入 `story-writer-runtime`、Human Writing L2、Main 工作流，也不修改任何现有生产链。

## 唯一目标

> 输入“已经确定要发生什么”，输出“读起来像真人作者写的中文小说正文”。

这里只研究**字怎么写好**。

不研究选题、大纲、爽点、世界观、Tracking、商业运营或 AI 检测率。

## 核心判断

旧式 AI 小说系统很容易把精力放在禁词、AI pattern、短句比例和多轮润色上。

这些只能减少表面问题，不能稳定告诉 Writer：

- 人物此刻先注意什么；
- 旁白什么时候该靠近人物；
- 一句普通中文怎么自然接到下一句；
- 对白怎么像人在做事；
- 哪些地方应该一句带过；
- 真人 Voice 到底体现在哪些反复选择里。

Prose Engine V1 因此只保留正向正文机制。

## 正常 WRITE

```text
PROSE_PACKET
  ↓
Context Compiler
  ↓
WRITER_CONTEXT
  + WRITE_CORE
  + ACTIVE_VOICE_CONTEXT（可空）
  ↓
First Draft
  ↓
Blind Reader
  ↓
REPAIR_PACKET（仅有真实 finding 时）
  ↓
One Local Repair
  ↓
Final Prose
```

### 第一稿只写，不审

Writer 不边写边扮演 Reviewer。

第一稿运行时主要是：

- 当前故事事实；
- POV 当前意识；
- 自然中文核心；
- 少量真人 Voice 证据。

研究资料、完整大纲、完整 Voice Profile、审稿报告都不进入默认 Writer 上下文。

### Blind Reader 与 Repair 分离

Blind Reader 没有改稿权，只报告真实阅读摩擦。

Repair 只能拿到最小 `REPAIR_PACKET`，最多一次局部修改。

目标不是“整体更漂亮”，而是让一个具体摩擦消失，同时不破坏已经成立的部分。

## 三个正式模式

### WRITE

写当前正文。

### DISTILL_VOICE

`Approved Human Prose → Contrastive Distillation → VOICE_PROFILE + Anchor Index`

只学习真人声音，不写新剧情。

### LEARN_FROM_EDIT

`AI Before + Human Approved After → Language-choice Diff → Voice Update Proposal`

只从真实修改学习。

详细见 `architecture/RUN_MODES.md`。

## Truth、Register、Voice 分开

### Truth

`PROSE_PACKET` 只负责：

- POV；
- 当前场景；
- 必须发生；
- 不能发生；
- 人物知道/不知道什么；
- end state；
- stop point。

策划术语不能成为正文语言。

### Register

`genre != register`。

修仙、玄幻、古代只决定必要题材词，不能自动把普通叙述和对白变成半文半白或“古风仙侠腔”。

Register 只有两种合法来源：

1. 用户明确指定；
2. approved Voice evidence。

### Voice

声音证据不是一个“克制、短句、网文感”的形容词列表。

它来自真人或用户真正认可的正文选择。

证据强度默认：

```text
user_correction > user_written / human_reference > accepted_project
```

`accepted_project` 主要服务项目连续性，不能因为“没被退稿”就自动升级成全局作者偏好。

## 真人 Anchor

每次生成只召回少量功能相近 anchor。

优先级：

1. 当前语言功能；
2. 互动结构；
3. 叙事距离；
4. prose mode；
5. Correction / Project Voice；
6. 题材与内容相似。

所以“收到坏消息后确认”可以跨题材召回。

“都是修仙”本身不是强匹配。

Anchor 学：

- 句子怎么运动；
- 人物声音怎么进入；
- 信息在哪停；
- 哪里故意写普通。

不借剧情、专名、比喻或原句。

## Contrastive Voice Distillation

不直接对母本说“总结一下文风”。

默认：

```text
Human Sample
  → Semantic Skeleton
  → Neutral Baseline
  → Human vs Baseline Contrast
  → Claim + Evidence
  → Cross-sample Clustering
  → Scope / Domain Filter
  → Voice Profile
```

这样尽量把“怎么写”从“写了什么”中剥离出来。

## 正文底层原则

### 人物注意力优先

不是：

`背景 → 原因 → 风险 → 方案 → 结论`

而是跟着人物实际经历移动。

人物可以只想到眼前一层，先做事，再回来判断。

### 叙事距离会动

重要决定、危险、欲望、异常时允许靠近 POV；重复劳动、时间经过、物流信息可以拉远。

### 中文先自然

现代自然中文白话是默认地基。

题材词可以专业或古老，普通动作、判断、对白不能为了“像小说”重新发明搭配。

### 普通句有价值

大量句子只负责把读者送到下一拍。

没有必要让每句话都变成金句、段尾落锤或可截图表达。

### 对白是互动

人物在问、拒绝、试探、催促、掩饰、推责、顶嘴，而不是配合作者把设定说完。

### 细节有选择

只在真正改变判断、人物、空间、风险、关系或下一动作时花细节。

重复过程可以直接概括。

## 解码策略

正文不是唯一正确答案任务。

如果模型接口支持采样控制，Writer 不默认用纯 greedy / beam / temperature=0。

但具体 temperature、top-p、min-p 等参数不写死在框架里，而放到具体模型适配层。

分析器和 Blind Reader 偏稳定，Writer 允许适度语言选择空间。

详细见 `architecture/DECODING_POLICY.md`。

## 文件结构

```text
standalone/prose-engine-v1/
├── README.md
├── MANIFEST.md
├── SKILL.md
├── architecture/
│   ├── CONTEXT_COMPILER.md
│   ├── DECODING_POLICY.md
│   ├── MODEL_ROLES.md
│   ├── PIPELINE.md
│   └── RUN_MODES.md
├── runtime/
│   ├── WRITE_CORE.md
│   ├── BLIND_READER_CORE.md
│   └── LOCAL_REPAIR_CORE.md
├── specs/
│   ├── PROSE_PACKET.md
│   ├── PROSE_QUALITY.md
│   ├── REPAIR_PACKET.md
│   ├── VOICE_CORPUS.md
│   ├── VOICE_PROFILE.md
│   └── ACTIVE_VOICE_CONTEXT.md
├── references/
│   ├── chinese-prose-base.md
│   ├── sentence-and-paragraph-motion.md
│   ├── scene-writing.md
│   ├── detail-and-compression.md
│   ├── character-consciousness.md
│   ├── dialogue-and-handoffs.md
│   ├── voice-system.md
│   ├── voice-distillation.md
│   ├── anchor-retrieval.md
│   ├── voice-validation.md
│   ├── learning-loop.md
│   ├── prose-generation-loop.md
│   └── cold-reader.md
└── research/
    ├── DESIGN_DECISIONS.md
    └── EVALUATION_AND_DIVERSITY.md
```

`research/` 永远不是运行时上下文。

## 当前状态

```yaml
status: DESIGN_ONLY
production_integration: NONE
modifies_story_writer_runtime: NO
modifies_human_writing_l2: NO
modifies_main_workflow: NO
learns_from_raw_ai_draft: NO
ai_detection_as_goal: NO
```

现在它仍然只是独立正文引擎设计，不接生产链。
