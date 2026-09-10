---
name: prose-engine-v1
status: design-only
purpose: human-like Chinese fiction prose generation from approved story semantics
---

# Prose Engine V1

## 唯一职责

把“已经确定会发生什么”写成**自然、好读、有人物意识的中文小说正文**。

不负责剧情规划、世界观、伏笔、Tracking、商业分析或 AI 检测率。

## 运行原则

这个 Skill 只做路由，不把所有写作方法一次塞给 Writer。

详细 references 使用 progressive disclosure：

- 正常 WRITE 只加载一个紧凑写作核心 + 当前场景包 + 少量 Voice Context。
- 只有出现明确问题时，才读取对应专项 reference。
- DISTILL_VOICE 与 LEARN_FROM_EDIT 是独立模式，不和 WRITE 混跑。

详细模式见 `architecture/RUN_MODES.md`。

## 模式

### WRITE

默认模式。

必读：

1. 当前 `PROSE_PACKET`。
2. `runtime/WRITE_CORE.md`。
3. 当前 `ACTIVE_VOICE_CONTEXT`，如果存在。

然后按：

`Semantic Wash → Scene Frame → Lived Draft → Blind Reader → One Local Repair`

执行。

正常第一稿**不要默认把 references/ 全部读一遍**。

### DISTILL_VOICE

只在需要从 approved human prose 建立/更新声音时使用。

读取：

- `references/voice-distillation.md`
- `references/voice-system.md`
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

## WRITE 的专项路由

默认先靠 `runtime/WRITE_CORE.md` 完成。

只有发生以下情况才加读详细 reference：

### 中文搭配 / 句子本身不顺

读取：

- `references/chinese-prose-base.md`
- `references/sentence-and-paragraph-motion.md`

### 人物像分析机器人 / 叙事离人物太远

读取：

- `references/character-consciousness.md`
- `references/scene-writing.md`

### 对白像信息广播 / 两个人太配合

读取：

- `references/dialogue-and-handoffs.md`

### 细节过多 / 身体反应堆叠 / 该快的地方写太慢

读取：

- `references/detail-and-compression.md`

### Voice 漂移 / 不知道该召回什么真人片段

读取：

- `references/voice-system.md`
- `references/anchor-retrieval.md`

### 整段生成方式失控

读取：

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

输入里的策划词只传意思，不是正文措辞样本。

## Voice

声音证据优先级：

`Correction Voice > Project Voice > Author Voice`

生成时只允许一个紧凑 `ACTIVE_VOICE_CONTEXT`：

- 3-5 条 active traits；
- 2-4 个 approved human anchors；
- 0-2 条当前 drift warnings。

Raw AI draft、被拒绝稿、outline、analysis、review 文本永远不能成为正向 Voice。

没有 Voice 时使用自然中文基线，不虚构作者风格。

## Blind Reader

完整段落/场景初稿后执行一次盲读。

Blind Reader 只能看到：

- 正文；
- 目标读者；
- 极少数阅读必需的专名说明。

看不到：

- PROSE_PACKET；
- Scene Frame；
- Voice Profile；
- 作者意图；
- Writer 自检。

它只判断：

- Flow；
- Presence；
- Character Mind；
- Language Pleasure；
- Pull。

详细规则见 `references/cold-reader.md`。

最多一次局部返修，不追求 finding=0。

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

## 模型角色

见 `architecture/MODEL_ROLES.md`。

允许 Writer、Voice Analyst、Blind Reader 使用不同模型。

框架不写死具体模型。

## 研究文档

`research/` 只解释为什么这么设计。

**运行时禁止加载 research 文件。**

## 当前状态

```yaml
status: DESIGN_ONLY
production_integration: NONE
modifies_existing_runtime: NO
modifies_human_writing_l2: NO
modifies_main_workflow: NO
learns_from_raw_ai_draft: NO
```