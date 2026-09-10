# Context Compiler

## 目的

把上游剧情语义和长期 Voice 资料编译成 Writer **这一次真正需要看的最小上下文**。

Context Compiler 不写正文，也不评价正文。

它只负责两件事：

1. 保留不可变的故事真相与当前场景；
2. 删除会把 Writer 带回策划腔、分析腔、方法论腔的上下文噪音。

## 输入

允许读取：

- `PROSE_PACKET`；
- 必要的上一段正式正文；
- `VOICE_PROFILE`；
- approved Voice Corpus / anchor index；
- 已确认的用户语言偏好；
- 当前 Writer 的重复 drift warning。

第一稿禁止读取：

- 完整大纲；
- 商业分析；
- 爽点说明；
- 审稿报告；
- research 文档；
- 被拒绝 AI 草稿；
- 旧版全过程思考；
- “为什么这样设计”的解释。

## 输出

```yaml
WRITER_CONTEXT:
  immutable_truth:
    pov: ""
    location: ""
    must_happen: []
    must_not_happen: []
    knowledge_boundary: []
    end_state: ""
    stop_point: ""

  scene_now:
    current_action: ""
    notices_first: ""
    immediate_want: ""
    immediate_pressure: ""

  prose_target:
    reader: ""
    reading_feel: ""
    pace: ""
    distance_bias: ""

  adjacent_prose:
    previous_tail: ""

  active_voice:
    traits: []
    anchors: []
    drift_warnings: []
```

Writer 不需要知道这些字段是怎么推导出来的。

## Semantic Wash

上游常见词：

`爽点 / 杠杆 / 门槛 / 功能位 / 升级 / 情绪曲线 / 信息差 / 压力来源 / 回报 / 冲突升级`

这些词只能被还原成可写事实。

例如：

- `制造身份压制` → 谁有权拒绝谁、谁必须等、谁能决定结果；
- `强化资源压力` → 还剩多少、什么时候要用、缺了会怎样；
- `形成爽点` → 人物做了什么，现实给出什么结果。

Semantic Wash **不能新增解释**，也不能把策划词换成另一套抽象词。

## Scene-Now 压缩

只保留会改变第一段和下一拍的信息。

如果一个背景事实在当前人物行动前完全用不到，就不进入 `scene_now`。

这样 Writer 不会因为“知道得太多”而在第一段主动解释。

## Voice Resolve

Voice 召回不按“同题材”优先，而按“同语言功能”优先。

推荐顺序：

1. 当前语言功能；
2. 当前互动结构；
3. 叙事距离；
4. prose mode；
5. Correction / Project Voice；
6. 内容或题材相似。

语言功能示例：

- 接到坏消息后确认；
- 熟人之间互相试探；
- 突然发现异常；
- 做完验证后下决定；
- 高压下只回一句；
- 走流程时心里另有打算；
- 一段重复劳动快速略过。

“都是修仙”“都在宗门”“都有系统”不能单独构成高质量 Voice 匹配。

## Anchor 防污染

Anchor 的主要作用是提醒 Writer：

- 句子怎么运动；
- 人物声音怎么进入；
- 哪里故意写普通；
- 信息写到哪里停。

Anchor 不能作为：

- 新剧情来源；
- 新动作来源；
- 比喻素材库；
- 专名库；
- 句式复制模板。

如果 anchor 与当前故事事实冲突，故事事实无条件优先。

## 上下文预算

当上下文超预算时，按以下顺序保留：

1. `immutable_truth`，不可裁；
2. `scene_now`，不可裁；
3. 精确 stop point，已包含于 truth；
4. 必要 previous tail；
5. 3 条最相关 Voice trait；
6. 2 个最相关 anchor；
7. drift warning；
8. 其他 Voice；
9. 专项 craft reference。

永远不要为了保留 style reference 而压缩故事边界。

## 设计原则

Writer 上下文越接近下面这个比例越健康：

```text
当前场景事实 > 人物当前意识 > 少量真人声音证据 > 写作方法
```

如果“写作方法”比“正在发生的事”更占上下文，说明 Context Compiler 失败。
