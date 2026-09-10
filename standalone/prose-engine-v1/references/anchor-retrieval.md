# Voice Anchor Retrieval

## 为什么需要锚点

抽象文风词只能给方向，不能稳定告诉模型“这一句怎么落”。

真实正文样本提供的是分布：句子通常多长、动作和判断怎么接、人物什么时候进入内心、对白后接什么、哪些地方作者故意写得很普通。

因此 Prose Engine 不只读取一个 Style Summary。它还要在写当前场景前，召回少量**功能相近的真人正文锚点**。

## 一、声音证据分三层

### A. Author Voice

跨项目稳定声音。

来源：用户明确认可的真人作者样本、用户自己的既有作品、用户授权的母本。

适合学习：

- 句子运动；
- 基础词汇与语域；
- 叙事距离倾向；
- 心理进入方式；
- 对白衔接；
- 普通度；
- 段落切换。

### B. Project Voice

当前作品已经正式接受的正文。

它回答：同一个人的声音到了这本书里以后，具体怎么变。

例如同一作者在轻松都市和压抑悬疑里的句长、幽默、内心密度会不同。

### C. Correction Voice

用户对 AI 正文做出的明确修改。

这是最高优先级证据，因为它直接说明“模型哪里写偏了，用户真正要什么”。

只有重复出现或被用户明确认可的修改倾向才进入长期 Voice；一次性剧情改动不进入。

## 二、不要直接把整本母本塞给 Writer

先把语料切成“可召回片段”。每个片段附功能标签，而不是只按章节切。

建议标签：

```yaml
scene_function:
  - bad_news
  - decision
  - confrontation
  - quiet_dialogue
  - discovery
  - action
  - transition
  - cultivation
  - aftermath
  - humor
  - explanation
pov_distance: close | medium | far | mixed
prose_mode:
  - action_led
  - dialogue_led
  - interiority_led
  - summary_led
  - mixed
emotion_pressure: low | medium | high
speaker_mix: solo | two_person | group
```

标签只用于召回，不应该出现在正文 prompt 里变成写作术语污染。

## 三、召回优先级

写当前场景前，根据当前 `PROSE_PACKET` 选 2-4 个锚点。

优先顺序：

1. **功能相似**：例如“看到坏消息后立刻判断”优先于“同样发生在宗门”。
2. **叙事模式相似**：对白场景找对白锚，内心决策找内心锚。
3. **当前项目优先**：正式 PASS 的本书正文优于跨项目母本。
4. **用户修改优先**：与当前 defect 相似的用户改稿优先。
5. **内容相似最后**：专名和题材相似不等于声音相似。

## 四、每个锚点只提三件事

Writer 不需要把锚点分析成十几条规则。

每个锚点最多提取：

```yaml
motion: "句子/段落怎么向前走"
voice_move: "人物声音怎样进入旁白或对白"
plain_move: "哪里故意写得普通"
```

必要时再附一条：

```yaml
avoid: "这个锚点没有做什么"
```

例如：

- 没有先解释人物全部处境；
- 没有把三个方案列完；
- 没有每句都配动作标签；
- 没有为了紧张连续砸短句。

## 五、锚点的使用方式

禁止逐句仿写。

正确使用方式是先读锚点，再关闭词面模仿意识，只保留“运动方式”。

例如学习到：

`坏消息出现 → 人物先确认 → 对方补一句 → 人物做决定`

不能把原文里的句式、比喻、专名、动作顺序照搬。

## 六、没有锚点时怎么办

没有 approved prose source 时：

1. 使用 `Chinese Prose Base`；
2. 使用场景协议与叙事距离控制；
3. 明确 `voice_confidence: low`；
4. 不凭空发明“作者风格”。

第一次获得用户认可正文后，再开始建立 Project Voice。

## 七、召回输出格式

```yaml
VOICE_CONTEXT:
  confidence: low | medium | high
  source_mix:
    author_voice: []
    project_voice: []
    correction_voice: []
  active_traits:
    - ""
    - ""
    - ""
  anchors:
    - source_id: ""
      function: ""
      motion: ""
      voice_move: ""
      plain_move: ""
```

`active_traits` 最多保留 5 条。

超过这个数量说明召回没有完成压缩，Writer 会重新掉进 checklist 写作。