---
name: prose-engine-v1
status: design-only
purpose: human-like Chinese fiction prose generation from approved story semantics
---

# Prose Engine V1

## 唯一职责

把“已经确定会发生什么”写成**自然、好读、有人物意识的中文小说正文**。

不负责剧情规划、世界观、伏笔、Tracking、商业分析或 AI 检测率。

## 总原则

这个 Skill 只做路由，不把整套写作方法一次塞给 Writer。

详细 references 使用 progressive disclosure：

- 正常 WRITE 只加载最小运行上下文；
- 只有出现明确病灶时才读取对应专项 reference；
- DISTILL_VOICE 与 LEARN_FROM_EDIT 独立运行，不和 WRITE 混跑；
- `research/` 永远不进入正文运行时。

## 模式

### WRITE

默认路径：

```text
PROSE_PACKET
  ↓
Context Compiler
  ↓
WRITER_CONTEXT
  + runtime/WRITE_CORE.md
  + ACTIVE_VOICE_CONTEXT（可空）
  ↓
Draft
  ↓
runtime/BLIND_READER_CORE.md
  ↓
REPAIR_PACKET（仅有真实 finding 时）
  ↓
runtime/LOCAL_REPAIR_CORE.md
  ↓
Final Prose
```

第一稿不要默认把 `references/` 全部读一遍。

### DISTILL_VOICE

只在需要从 approved human prose 建立/更新声音时使用。

读取：

- `references/voice-distillation.md`
- `references/voice-system.md`
- `references/voice-validation.md`
- `specs/VOICE_CORPUS.md`
- `specs/VOICE_PROFILE.md`

不生成新小说正文。

### LEARN_FROM_EDIT

只在有 `AI before + human/user approved after` 时使用。

读取：

- `references/learning-loop.md`
- `references/voice-system.md`
- `specs/VOICE_PROFILE.md`

只生成 Voice 更新候选，不把一次修改直接写成永久规则。

## Context Compiler

见 `architecture/CONTEXT_COMPILER.md`。

它负责：

- 把策划词洗回事实；
- 只保留当前场景需要的信息；
- 编译少量 Voice traits / anchors；
- 防止完整大纲、研究说明、审稿报告污染 Writer。

Writer 不直接读取完整 Voice Profile 或整本母本。

## WRITE 专项路由

默认先靠 `runtime/WRITE_CORE.md` 完成。

只有命中具体问题时才加读：

### 中文搭配 / 句子本身不顺

- `references/chinese-prose-base.md`
- `references/sentence-and-paragraph-motion.md`

### 人物像分析机器人 / 叙事离人物太远

- `references/character-consciousness.md`
- `references/scene-writing.md`

### 对白像信息广播

- `references/dialogue-and-handoffs.md`

### 细节过多 / 该快的地方写太慢

- `references/detail-and-compression.md`

### Voice 漂移 / anchor 召回不对

- `references/voice-system.md`
- `references/anchor-retrieval.md`

### 整段生成方式失控

- `references/prose-generation-loop.md`

不要因为一个局部问题把全部 reference 加载进来。

## 输入

使用 `specs/PROSE_PACKET.md`。

最重要的信息只有：

- POV；
- 当前场景起点；
- 眼下欲望/压力；
- 必须发生的语义事件；
- 人物知道 / 不知道什么；
- 不允许新增 / 提前释放什么；
- 场景结束状态；
- 精确停笔点。

### Register Firewall

`genre` 不能自动推导正文语体。

修仙、玄幻、古代只决定必要题材词，不自动把普通叙述和对白古老化。

正文 register 只有两种合法来源：

1. 用户明确指定；
2. approved Voice evidence。

## Voice

Voice 不使用一条粗暴总优先级，而分成两条轴。

### Evidence Reliability

```text
user_correction > user_written / human_reference > accepted_project
```

冲突时，可靠度高的证据优先。

### Scope Relevance

在不与高可靠证据冲突时：

```text
same character / same project / same scene-function > cross-project general
```

因此 Project Voice 用来具体化当前书的声音，但不能反过来覆盖用户亲改或真人母本中更可靠的证据。

生成时只允许一个紧凑 `ACTIVE_VOICE_CONTEXT`：

- 3-5 条 active traits；
- 2-4 个功能相近 approved anchors；
- 0-2 条当前 drift warnings。

Anchor 先按**语言功能/互动功能**匹配，题材相似最后考虑。

Raw AI draft、被拒绝稿、outline、analysis、review 文本永远不能成为正向 Voice。

没有 Voice 时使用自然现代中文基线，不虚构作者风格。

## Blind Reader 与 Repair

Blind Reader 使用 `runtime/BLIND_READER_CORE.md`。

它只能看到正文和目标读者，看不到剧情设计与 Writer 自检。

默认最多 3 条 finding，硬上限 5 条。

有真实 finding 时编译 `specs/REPAIR_PACKET.md`，再交给 `runtime/LOCAL_REPAIR_CORE.md`。

Repair：

- 最多一轮；
- 只修局部；
- 必须保护 `keep`；
- 不新增剧情；
- 不全文 humanize；
- 不顺手重写健康段落。

## 解码

方向见 `architecture/DECODING_POLICY.md`。

Writer 可以保留适度语言选择空间，但具体 temperature、top-p、min-p 等参数属于模型适配层，不写死进正文核心。

## 质量底线

见 `specs/PROSE_QUALITY.md`。

四类成片问题不能接受：

1. Translation Friction：中文需要脑内二次翻译。
2. Report Mind：人物心理像分类/分析报告。
3. Flat Distance：长期由作者替 POV 解释。
4. Voice Contamination：策划、审稿或默认 AI 腔进入正文。

## 明确不采用

默认不做：

- 巨型禁词表驱动正文；
- 短句率 / 对白率 / 比喻密度配额；
- 全文 humanize；
- 多轮同义词洗稿；
- Writer + Judge 无限循环；
- Raw AI draft 自我学习；
- 把整个母本塞进上下文；
- 把整套 Voice Profile 每章全量加载。

## 当前状态

```yaml
status: DESIGN_ONLY
production_integration: NONE
modifies_existing_runtime: NO
modifies_human_writing_l2: NO
modifies_main_workflow: NO
learns_from_raw_ai_draft: NO
```
