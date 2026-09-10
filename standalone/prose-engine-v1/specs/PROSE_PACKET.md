# PROSE_PACKET Contract

## 目的

让 Prose Engine 可以完全脱离现有小说工作流运行。

调用者只需要把“已经确定的剧情语义”压成这个包。Prose Engine 不需要知道这些语义来自大纲、聊天、数据库还是另一个 AI。

## 最小输入

```yaml
PROSE_PACKET:
  language: zh-CN
  genre: ""
  audience: ""
  length_hint: ""

  prose:
    register: "现代自然中文白话 / 用户明确指定语体 / 空"
    pace: ""
    distance_bias: close | mixed | far | ""

  pov:
    person: first | third_limited | third_omniscient
    character: ""

  scene:
    start:
      place: ""
      time: ""
      current_action: ""
      attention_seed: "人物最先注意到什么，可空"
    immediate_want: ""
    immediate_pressure: ""
    beats:
      - "必须发生的语义事件 1"
      - "必须发生的语义事件 2"
    end_state: ""
    stop_point: ""

  knowledge:
    pov_knows:
      - ""
    pov_does_not_know:
      - ""

  constraints:
    must_keep:
      - ""
    must_not_add:
      - ""
    must_not_reveal:
      - ""

  characters:
    - name: ""
      relation: ""
      current_state: ""
      speech_note: ""

  voice:
    profile_id: ""
    approved_sample_ids: []
    explicit_preferences: []

  reader:
    target: ""
```

## 设计原则

### 1. 只传“会影响正文正确性”的事实

不要把整套世界观、全书人物卡、所有伏笔一起送进来。

信息越多，Writer 越容易回到总结/说明模式。

### 2. genre 不等于 register

这是硬规则。

`genre: 修仙 / 玄幻 / 古代 / 克苏鲁 / 科幻` 只帮助理解世界和题材名词，**不能自动推导正文语体**。

例如：

- 修仙名词可以是“炼气、灵石、宗门”；
- 但普通叙述、人物判断和对白仍默认使用现代中国读者第一次就能顺读的白话。

只有两种证据可以改变 register：

1. 用户明确指定；
2. approved Voice evidence 明确支持。

不得因为题材自行加入：

- 半文半白；
- 古老化措辞；
- 生造仙侠词组；
- “似有若无、眸光微凝、心下了然”式默认题材腔。

### 3. beats 只能写语义

好：

`林砚在公示名单上发现自己的名字被提前了一批。`

不好：

`用短句制造震惊感，让名单数字承担压力，然后通过内心独白突出危机。`

后一种属于写法设计，不属于剧情语义。

### 4. attention_seed 只是现场起点

它可以为空。

如果明确知道人物最先注意什么，就写事实：

- “名单上自己的名字”；
- “门外有人敲门”；
- “手里符纸突然发热”。

不要写：

- “通过视觉细节建立危机感”；
- “先制造异常感再推进”。

### 5. speech_note 只写稳定人物差异

例如：

- “说话直接，少客套”；
- “面对上级时会收着，不主动顶撞”；
- “熟人之间会带一点损话”。

不要写：

- 每句不超过 15 字；
- 每三句必须有动作；
- 对白占比 30%。

### 6. length_hint 是软目标

可以写：

- “约 1200-1600 中文字”；
- “一个完整短场景”；
- “只写到他推门出去”。

如果字数与自然停点冲突，优先停在已指定 `stop_point`。

### 7. voice 可以为空

如果没有任何 approved voice source，允许：

```yaml
voice:
  profile_id: null
  approved_sample_ids: []
  explicit_preferences: []
```

此时使用自然现代中文基线，绝不偷偷从未审核 AI 稿里构造“作者声音”。

## 传入前清洗

调用者最好提前移除：

- 爽点；
- 杠杆；
- 情绪曲线；
- 信息差；
- 节奏加速；
- 读者奖励；
- 功能位；
- scene goal / beat function 等方法论标签。

如果无法移除，Prose Engine 的 Semantic Wash 必须先把它们转换回事件事实，再开始正文生成。
