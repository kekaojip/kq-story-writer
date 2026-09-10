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
  scene_function: []
  prose_mode: []
  pov_distance: close | medium | far | mixed
  emotion_pressure: low | medium | high
  speaker_mix: solo | two_person | group
  character_scope: ""
  project_scope: ""
  tags: []
```

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

检索索引应该优先支持：

1. scene_function；
2. prose_mode；
3. narrative distance；
4. speaker mix；
5. pressure；
6. semantic embedding；
7. genre/domain。

语义 embedding 是辅助，不是唯一检索。

原因：两个片段都谈“宗门名单”不代表语言功能一样；一个“现代职场收到裁员名单”的反应段，可能比另一个修仙设定介绍段更适合作为正文运动锚点。

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
- 功能标签准确；
- 能在当前场景召回对的几段；
- 不让 AI 自己的默认腔进入正向训练循环。