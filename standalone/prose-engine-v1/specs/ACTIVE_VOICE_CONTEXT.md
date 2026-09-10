# ACTIVE_VOICE_CONTEXT Contract

## 目的

把完整 Voice Profile 和语料库压成 Writer **这一次真正需要看到的极小声音上下文**。

Writer 不直接读取整套 Voice Corpus。

## 格式

```yaml
ACTIVE_VOICE_CONTEXT:
  voice_id: ""
  confidence: low | medium | high

  traits:
    - dimension: "sentence_motion | narrative_distance | interiority | diction | dialogue | paragraph | plainness"
      principle: ""

  anchors:
    - anchor_id: ""
      source_type: human_reference | user_written | accepted_project | user_correction
      function: ""
      motion: ""
      voice_move: ""
      plain_move: ""
      excerpt_locator: ""

  drift_warnings:
    - ""
```

## 数量限制

默认：

- `traits`: 3-5 条；
- `anchors`: 2-4 个；
- `drift_warnings`: 0-2 条。

这是上下文预算，不是文风统计配额。

如果当前场景没有足够相关证据，宁可少给，不要用无关 trait 填满。

## Traits 怎么选

优先选择会改变**当前场景落字**的 trait。

例如当前是两人高压对话，可能需要：

- dialogue handoff；
- narrative distance；
- plainness；
- sentence motion。

不需要把环境描写、战斗节奏等无关 trait 一起带上。

## Anchors 怎么选

召回优先级：

1. 当前语言功能相似；
2. prose mode 相似；
3. Correction / Project Voice 优先；
4. POV distance 相似；
5. 内容/题材相似。

Anchor 给 Writer 的主要不是原文，而是：

- `motion`：句子怎样向前；
- `voice_move`：人物声音怎样进入；
- `plain_move`：哪里故意不加工。

`excerpt_locator` 允许运行环境临时读取极短 approved 原文片段。若版权/隐私或运行环境不允许，则只使用上面三项分析，不复制原文。

## Drift Warning

只放当前 Writer 模型对这个用户/项目**反复出现**的偏航。

好：

- “高压决策时不要把心理整理成资源/方案清单。”
- “close POV 中模型常多加‘他意识到’，当前优先直接判断。”

不好：

- “禁止比喻。”
- “不要 AI 味。”
- “不要写得不好。”
- 一整套通用禁词表。

## 没有 Voice 时

允许：

```yaml
ACTIVE_VOICE_CONTEXT:
  voice_id: null
  confidence: low
  traits: []
  anchors: []
  drift_warnings: []
```

此时 Writer 只靠 `WRITE_CORE` 的自然中文基线和当前人物/场景写作。

不要拿未审核 AI 稿补空缺。

## 生命周期

ACTIVE_VOICE_CONTEXT 是一次性编译产物。

写完当前场景后可以丢弃。

长期真相仍在：

- VOICE_CORPUS；
- VOICE_PROFILE；
- approved correction evidence。

这样可以避免每章把临时场景选择误记成永久作者风格。