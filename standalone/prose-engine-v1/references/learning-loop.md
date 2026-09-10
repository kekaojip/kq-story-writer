# Learning Loop

## 目标

让模块随着用户真正的选择变准，而不是随着 AI 自己生成的文本越来越像自己。

核心规则：

> Learn from reviewed human decisions, not from raw AI drafts.

## 三层学习来源

### 1. Correction Voice，最高优先级

用户对 AI 正文的明确修改。

但先过 significance filter，只保留真正改变写法的 edit。

跳过：

- 标点；
- 错别字；
- 专名；
- 单次事实；
- 为当前剧情临时补一句信息。

保留：

- 改变叙事距离；
- 改变心理进入方式；
- 改掉不自然搭配；
- 删除解释尾巴；
- 改变对白衔接；
- 改变段落换手；
- 把抽象词换成人物自己的普通词；
- 把方案清单拆回现场思考。

### 2. Project Voice

本项目正式接受的正文。

只在正文被真正接受后进入。

项目 Voice 代表“这本书里的声音”，不能自动覆盖跨项目 Author Voice。

### 3. Author Voice

用户提供或批准的跨项目真人样本。

它变化最慢，用来保留底层语言习惯。

## AI 草稿的地位

AI 原始 draft 永远不是正向声音证据。

它只能提供：

- 被修改前的负例；
- 与用户修订版的 diff；
- 反复出现的模型 drift 统计。

AI 写 → AI 审 → AI 通过，不能形成学习闭环。

## 从 diff 学习，不从理由作文学习

学习时优先看真实 before / after。

例如：

Before:
`他意识到事情比想象中严重得多。`

After:
`这事比他想的麻烦。`

候选学习：

- 贴 POV 时偏好直接判断；
- 少用“意识到”引导；
- 抽象程度词优先换成人物会用的普通词。

不要记剧情内容。

## Pattern Proposal

每次 significant edits 先进入待聚合区，不立刻写入 Voice Profile。

建议格式：

```yaml
EDIT_SIGNAL:
  dimension: narrative_distance | diction | dialogue | paragraph | interiority | explanation | rhythm | other
  before_pattern: ""
  after_pattern: ""
  scope_guess: global | project | character | scene_type
  confidence: low | medium | high
```

## 升级条件

候选 trait 至少满足一个条件才进入正式 Voice：

1. 用户明确说“以后就按这个”；
2. 同类 edit 重复出现；
3. 与已批准真人样本中的稳定模式一致；
4. 在多个场景里都成立，而且不是剧情偶然。

不要用固定“10 次才算”作为死门槛。重复度只是证据，不是配额。

## 冲突处理

优先级：

`Correction Voice > Project Voice > Author Voice`

但必须先判断 scope。

例如：

- 作者平时少用长句；
- 当前项目在修炼感悟场景里偶尔使用较长句。

这不一定冲突，可能只是 scene_type 条件不同。

只有同一 scope 真正冲突时，才让更高优先级覆盖。

## Voice Memory 必须保持短

长期档案可以保存证据，但每次给 Writer 的 active memory 最多：

- 3-5 条 traits；
- 2-4 个 anchors；
- 0-2 条 drift warnings。

如果 active memory 越学越长，说明学习系统退化成规则仓库。

## Negative Drift Memory

模型反复出现、用户反复删除的问题，可以进入 `avoid_drift`。

例如：

- 分类列方案；
- 每段结算；
- 连续“他意识到”；
- 题材导致普通句做旧；
- 抽象名词替代普通动作。

但 negative memory 不能取代正向 Voice。

如果一个系统只知道不要写什么，它最后只会得到“干净但没声音”的正文。

## 最终原则

学习闭环不是为了让 AI 越来越像 AI 自己。

它应该让每一次用户真正点头的修改，都变成下一次更少需要解释的隐性选择。