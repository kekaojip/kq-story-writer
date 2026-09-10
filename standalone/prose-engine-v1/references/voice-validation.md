# Voice Validation

## 目的

防止 Voice Analyst 读几段文本后凭感觉发明“作者风格”。

Voice 蒸馏以 close reading 为主，但可以用轻量 stylometry 做旁证。

**统计只负责回答“这个模式真的稳定存在吗”，不负责告诉 Writer 必须写成什么比例。**

## 可验证维度

根据语料长度和工具能力选择，不要求全部计算。

### Sentence Shape

- 平均句长；
- 句长标准差 / 分布宽度；
- 长短句切换；
- 句首结构的重复度。

用途：验证“句子节奏稳定/变化大”之类 claim。

### Lexical Profile

- 长度鲁棒的词汇多样性；
- 高频普通动词；
- 抽象词 / 具体词倾向；
- 高频功能词与连接颗粒。

用途：验证“词汇朴素”“功能词使用有特征”等，不拿词频直接生成。

### Function Words

功能词比内容词更不容易被题材污染。

可观察：

- 的、了、着、过；
- 就、还、又、却、才；
- 常用代词；
- 常用连接方式。

如果工具支持，可用 function-word profile / Burrows-style distance 比较不同样本是否像同一声音方向。

### Syntactic Pattern

可观察：

- 主谓宾常见结构；
- 修饰密度；
- 从句/复句复杂度；
- 动作句与名词化表达；
- 常见句法模板。

### Paragraph Shape

- 单句段 / 短段 / 中长段分布；
- 段长变化；
- 对话段与叙述段交替。

只用来发现稳定习惯或 drift，不输出“必须 30% 单句段”这种要求。

## 验证流程

Voice Analyst 先提出：

```yaml
claim: "高压场景句长变化会明显增大，短判断常夹在连续动作之间。"
evidence_ids: [A12, A17, A24]
```

然后检查可量化旁证。

结果只分：

```yaml
validation: supported | mixed | unsupported | insufficient_data
```

### supported

定量/跨样本证据与 close reading 同方向。

### mixed

不同场景或不同作品表现不同，trait 应缩小 scope。

### unsupported

统计和跨样本检查不支持，不能升级为 stable Voice trait。

### insufficient_data

样本太少，保留为 uncertain。

## 不允许的用法

禁止：

- 用 stylometry 分数决定“好不好看”；
- 为了匹配 baseline 强制改正文；
- 把 z-score 变成生成配额；
- 因为句长平均数偏离就自动重写；
- 用 AI detector 当 Voice 验证器；
- 把题材内容词误当作者 idiolect。

## Drift Detection

Stylometry 更适合做**跨章节 drift 提示**：

例如：

- Project Voice 原本句长变化丰富，后 5 章突然全部收敛；
- 某个角色对白突然变得和其他人一样；
- 连接词 / 名词化结构突然激增；
- 旁白功能词分布和 accepted corpus 明显偏离。

这里只产生提示，不自动修。

最终仍要回到真实正文和用户读感判断原因。

## 核心原则

Voice 的证据链应该是：

`真人文本 → close reading claim → 跨样本证据 → 可选 stylometric validation → scoped trait`

而不是：

`统计数字 → 写作配方`。