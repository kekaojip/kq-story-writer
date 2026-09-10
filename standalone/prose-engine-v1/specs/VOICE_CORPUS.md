# VOICE_CORPUS Contract

## 目标

Voice Corpus 保存**可被 Prose Engine 学习的正文证据**。

它不是所有历史文本的垃圾桶。

最重要的边界：

> 原始 AI 草稿、被拒绝稿、未审核稿，不得进入正向 Voice Corpus。

## Source Types

```yaml
source_type:
  - human_reference      # 用户明确授权的真人作品样本
  - user_written         # 用户自己的原始正文
  - accepted_project     # 当前项目正式接受正文
  - user_correction      # 用户亲手修改并认可的版本
```

## Evidence Strength

来源不同，证据强度不能一样。

默认：

```text
user_correction  >  user_written / human_reference  >  accepted_project
```

### user_correction

最高信号。

它直接说明：模型原来怎么写，用户真正会怎么改。

可以用于建立/修正稳定 Voice trait，但仍需判断这次修改是不是一次性剧情需要。

### user_written / human_reference

强正向证据。

适合学习：

- 句子运动；
- 叙事距离；
- 对白衔接；
- 普通度；
- 语域；
- 段落换手。

### accepted_project

弱到中等证据。

它主要保证**当前项目连续性**，不能因为“用户没退稿”就自动证明这是一条全局作者偏好。

规则：

- 单独的 accepted_project 不得创建新的 global trait；
- 多章反复稳定 + 用户持续接受，才可提高置信度；
- 一旦与 user_correction / human reference 冲突，accepted_project 让位。

这样避免 AI 生成 → AI 被动通过 → AI 把自己学回去。

## Approval

每个 source 必须有明确状态：

```yaml
approval:
  status: approved | limited | rejected
  scope: global | project | character | scene_type
  note: ""
```

- `approved`：可进入正向 Voice 分析和 anchor retrieval。
- `limited`：只在指定 scope 使用。
- `rejected`：只可作为负面 drift evidence。

## Source Record

```yaml
VOICE_SOURCE:
  source_id: ""
  source_type: human_reference | user_written | accepted_project | user_correction
  evidence_strength: strong | medium | weak
  approval:
    status: approved | limited | rejected
    scope: global | project | character | scene_type
  provenance:
    title: ""
    author_or_owner: ""
    location: ""
    rights_note: ""
  text_location: "private/local/path-or-reference"
  language: zh-CN
  domain:
    genre: ""
    platform_or_register: ""
  quality_note: ""
```

原始长文本可以放在用户授权的私有/本地语料位置，不要求复制到公开仓库。

Voice Profile 中只保存证据 ID、提炼原则和必要短锚点位置。

## Anchor Unit

从 approved source 切出的可召回单元：

```yaml
VOICE_ANCHOR:
  anchor_id: ""
  source_id: ""
  span_locator: ""
  language_function: []
  scene_function: []
  interaction_shape: solo | two_person | group | none
  prose_mode: []
  pov_distance: close | medium | far | mixed
  emotion_pressure: low | medium | high
  character_scope: ""
  project_scope: ""
  tags: []
```

### language_function

这是召回最重要的字段之一，描述**这段文字在语言层真正做什么**。

示例：

- confirm_bad_news
- verify_result
- short_decision
- hesitate_then_act
- deflect_question
- familiar_teasing
- restrained_confrontation
- receive_order
- notice_anomaly
- compress_routine
- explain_only_as_needed
- aftermath_processing

标签是检索元数据，不进入正文 prompt 成为术语。

`span_locator` 指向原始语料，不需要把整段原文复制进索引文件。

## Anchor 切分原则

按**语言功能闭合点**切，而不是固定 500 字。

一个 anchor 最好能展示一种相对完整的写法选择，例如：

- 发现坏消息后的确认与反应；
- 两人熟人对话的一轮来回；
- 一个复杂决定如何进入心理；
- 战斗中动作与判断如何交替；
- 一段时间跳过；
- 一段设定解释怎样被当前事件需要。

过短看不出运动方式，过长会混进太多不同模式。

## Indexing

检索优先级：

1. language_function；
2. interaction_shape；
3. prose_mode；
4. narrative distance；
5. evidence strength / scope；
6. pressure；
7. semantic embedding；
8. genre/domain。

语义 embedding 是辅助，不是唯一检索。

原因：两个片段都谈“宗门名单”不代表语言功能一样；一个“现代职场收到裁员名单”的反应段，可能比另一个修仙设定介绍段更适合作为正文运动锚点。

## Retrieval Hygiene

如果语料足够：

- 不要让 4 个 anchor 全来自同一个长段；
- 优先避免内容高度相似但写法功能不相似的片段；
- Correction / Project scope 与当前问题直接相关时可以覆盖来源多样性要求；
- 召回不到好 anchor 时宁可少给，不凑数量。

## Negative Corpus

被拒绝的 AI 片段可以单独保存为 `DRIFT_CASE`：

```yaml
DRIFT_CASE:
  case_id: ""
  bad_span: ""
  user_feedback: ""
  corrected_span_id: ""
  inferred_drift:
    - ""
```

Negative Corpus 永远不参与正向 anchor retrieval。

它只帮助：

- Voice Analyst 发现模型反复犯什么；
- Correction Voice 从 before/after 提取真正偏好。

## Corpus Hygiene

定期检查：

- 同一段是否重复入库；
- AI 草稿是否误标 approved；
- 项目专属声线是否泄漏成 global；
- 单一母本是否占比过高导致过拟合；
- 低质量早期 accepted prose 是否应该降级；
- 用户后来明确改变偏好时，旧 evidence scope 是否需要更新。

## 核心原则

Voice Corpus 的价值不在“越多越好”。

价值来自：

- 来源可信；
- 用户真的认可；
- 证据强度分清；
- 功能标签准确；
- 能在当前场景召回对的几段；
- 不让 AI 自己的默认腔进入正向训练循环。
