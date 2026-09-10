# VOICE_PROFILE Contract

## 目标

Voice Profile 不是“短句 60%、比喻每千字 1 次”的配额表。

它是一个**从真人文本和用户修改中提炼出来的、可被 Writer 一次读懂的声音模型**。

必须同时保留：

- 稳定原则；
- 代表证据位置；
- 适用范围；
- 不确定性。

## 三类证据

```yaml
EVIDENCE:
  author_voice:
    # 跨作品真人样本
  project_voice:
    # 当前作品正式接受正文
  correction_voice:
    # 用户对 AI 的明确修改
```

冲突时优先级：

`Correction Voice > Project Voice > Author Voice`

原因：用户最近亲手纠正过的选择，比跨项目平均风格更能代表当前正文需要。

## Profile 推荐结构

```yaml
VOICE_PROFILE:
  id: ""
  confidence: low | medium | high

  core:
    sentence_motion:
      principle: ""
      evidence_ids: []
    narrative_distance:
      principle: ""
      evidence_ids: []
    interiority:
      principle: ""
      evidence_ids: []
    vocabulary_register:
      principle: ""
      evidence_ids: []
    dialogue_handoff:
      principle: ""
      evidence_ids: []
    paragraph_rhythm:
      principle: ""
      evidence_ids: []
    plainness:
      principle: ""
      evidence_ids: []

  conditional:
    - when: "高压动作场景"
      traits:
        - ""
    - when: "熟人对话"
      traits:
        - ""

  avoid_drift:
    - ""

  uncertain:
    - ""
```

不是每个项目都必须填满全部字段。没有证据就留空，不要为了完整性猜。

## 提取方法

### Stage 1：单片段观察

对每个 approved sample 只观察“怎么写”，不要总结剧情。

记录：

- 句子如何起步和转手；
- 何时进人物脑内；
- 何时拉远；
- 普通动作常用哪些自然搭配；
- 对白后通常接什么；
- 情绪是否命名、动作化、留白；
- 哪些地方刻意不修辞；
- 段落在哪些注意变化处切开。

### Stage 2：跨片段聚合

只保留重复出现的模式。

一次出现的漂亮句、独特意象、特殊桥段不能升级成 Voice Trait。

### Stage 3：区分“稳定声音”与“场景习惯”

如果一个模式只在战斗场景出现，就放入 conditional，不要宣称它是全局文风。

### Stage 4：负面漂移

`avoid_drift` 只存两类东西：

1. 用户明确拒绝过；
2. 相比真人样本，模型反复多出来的默认行为。

例如：

- 过度把判断整理成分类清单；
- 旁白长期停在中距离解释位；
- 每段用短句结算；
- 为题材感生造动宾搭配。

不要把泛用“AI 禁词大全”搬进 Profile。

## Correction Voice

用户修改是最高价值数据，但必须先过 significance filter。

以下不学习：

- 错别字；
- 标点；
- 专名修正；
- 单次剧情事实；
- 为当前场景临时补一句设定。

以下值得学习：

- 用户连续把“他意识到”改成直接判断；
- 用户连续删除解释性收束；
- 用户把抽象词换成日常动词；
- 用户反复把完整对白改成半句/打断/不回答；
- 用户反复改变段落切法。

同类修改出现多次，或用户明确说“以后就这样”，才升级为正式 trait。

## Profile 长度

最终给 Writer 的 active profile 必须短。

完整档案可以长，但每次生成只蒸馏出：

- 3-5 条 active traits；
- 2-4 个 anchor；
- 0-2 条当前场景 drift warning。

Writer 如果需要边写边翻几十条规则，说明 Profile 已经失败。