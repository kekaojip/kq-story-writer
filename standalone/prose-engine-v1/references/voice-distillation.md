# Voice Distillation

## 目标

从真人正文中提炼“写法”，而不是把剧情内容误当成文风。

最常见的失败是：

- 样本里有宗门 → Style 写成“偏好宗门感”；
- 样本里发生战斗 → Style 写成“节奏强烈”；
- 样本恰好短句多 → 直接规定以后都短句。

真正要蒸馏的是：**面对同一种叙事任务，这个作者通常怎么选择语言。**

## Source Gate

可进入蒸馏：

- 用户自己的作品；
- 用户明确批准作为文风源的文本；
- 当前项目正式接受正文；
- 用户亲手修改并认可的版本。

不得进入正向蒸馏：

- 未审核 AI 草稿；
- 被用户拒绝稿；
- 策划文档；
- 大纲；
- 审稿报告。

## Stage 1：Scene Segmentation

不要按固定字数切母本。

优先按功能切成可独立判断写法的片段：

- 一轮对话；
- 一个发现；
- 一次决定；
- 一段动作；
- 一个情绪反应；
- 一次转场；
- 一段解释；
- 一段修炼 / 战斗 / 日常操作。

每个片段记录 source_id，不在公开 Voice Profile 中永久复制长原文。

## Stage 2：Semantic Skeleton

对每个真人片段先抽取极简语义：

```yaml
SEMANTIC_SKELETON:
  pov: ""
  start: ""
  events:
    - ""
  relationship: ""
  emotion_pressure: ""
  end: ""
```

只描述发生什么，不复刻原句。

## Stage 3：Neutral Baseline

构造一个“普通、合格但没有该作者特色”的中性表达参照。

目的不是拿 Baseline 当成生成目标，而是帮助识别：

> 真人作者相对普通写法，稳定地改变了什么？

参照可以由分析模型根据同一个 Semantic Skeleton 生成，也可以使用同题材的中性 corpus 样本。

Neutral Baseline 不进入 Voice Memory。

## Stage 4：Contrastive Analysis

把 Human Sample 与 Neutral Baseline 比较，只找**可迁移差异**。

重点看：

### Sentence Motion

- 谁先出现：动作、判断、对白、环境？
- 一个信息用一句落还是几句落？
- 长短句在哪里切换？

### Narrative Distance

- 真人样本比 baseline 更近还是更远？
- 哪种情境会直接出现人物判断？
- 是否经常用“他想 / 他意识到”作为中介？

### Interiority

- 心理是标签、直接判断、自由间接、动作携带还是展开思索？
- 通常想到哪一层就停？

### Lexical Choice

- 常见动作偏好哪些普通动词？
- 抽象词多还是具体词多？
- 自然连接词如何使用？
- 对题材术语的密度和位置有什么规律？

### Dialogue Handoff

- 对白后接标签、动作、心理、下一句还是留白？
- 熟人之间省略多少共享信息？
- 冲突时是否直接回答？

### Paragraph Rhythm

- 哪种注意变化触发换段？
- 重点句是否独段？
- 普通段落怎样把读者送到下一拍？

### Plainness

- 真人作者哪些地方明显比 baseline 更简单、更普通？
- 哪些可写成修辞的地方他选择不写？

“没有做什么”是重要风格证据。

## Stage 5：Claim + Evidence

每个候选 trait 必须同时有：

```yaml
trait: ""
evidence_ids: []
contrast: "相对 neutral baseline 的稳定差异"
scope: global | project | character | scene_type
confidence: low | medium | high
```

禁止只有形容词没有证据。

例如：

坏：

`文风简洁克制。`

好：

`高压决策时通常先给可见事实，再直接落人物判断，少用“他意识到”引导；在 4 个独立片段中重复出现。`

## Stage 6：Cross-Sample Clustering

单片段观察不能直接升级成作者特征。

把多个片段中的 trait 聚合：

- 重复出现 → core；
- 只在某类场景出现 → conditional；
- 与题材强绑定 → domain-specific；
- 只有一次 → uncertain / 不进入 active profile。

## Stage 7：Domain Transfer Filter

区分：

- 作者真正的写法；
- 当前题材天然要求；
- 当前人物特有声线；
- 某一次剧情偶然。

例如修仙样本中“灵力、丹田、宗门”不是 Voice Trait。

但“写修炼时优先身体结果，极少抽象解释机制”可能是可迁移的 scene-type trait。

## Stage 8：Compact Voice Profile

最终保留：

- 稳定原则；
- 少量 evidence_id；
- conditional traits；
- avoid_drift；
- confidence notes。

真正生成时再从 Profile 中取 3-5 条 active traits 和 2-4 个 anchor。

## 重要限制

- 不把母本的长段原文永久复制到共享仓库；
- 不把独特比喻、金句、专名作为模板；
- 不做逐句风格克隆；
- 不把一次出现频率变成死配额；
- 不因为样本作者“写得好”就复制其所有习惯。

目标是学习**选择机制**，不是复制表面纹理。