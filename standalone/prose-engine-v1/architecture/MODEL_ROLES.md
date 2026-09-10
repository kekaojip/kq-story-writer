# Model Roles

## 原则

Prose Engine 不假设“一个最强模型包办所有事情”。

正文生成、文风蒸馏、盲读判断、局部返修需要的能力不同。

## Role 1：Prose Writer

### 任务

根据 `WRITER_CONTEXT + WRITE_CORE + Active Voice Context` 写正文。

### 最看重

- 中文句子自然；
- 小说叙事距离；
- 对白；
- 人物意识；
- 段落流动；
- 能容忍留白和不完整解释。

### 不要求

- 最强数学；
- 最强工具调用；
- 最强长链推理。

### 选择策略

优先实际正文表现，而不是模型总榜排名。

如果有专门中文网文 fine-tune，可以作为候选，但必须保留可替换接口。

不要把某个具体模型名写死进框架。

## Role 2：Voice Analyst

### 任务

- 真人样本语义抽骨；
- contrastive style analysis；
- 跨样本聚合；
- domain transfer 过滤；
- 用户 edit diff 提炼。

### 最看重

- 细读；
- 比较；
- 归纳；
- 能区分内容与写法；
- 不轻易把一次样本过拟合成规则。

这里通常可以使用更强的通用推理模型。

## Role 3：Blind Reader

### 任务

第一次只读正文，报告真实阅读体验。

### 最看重

- 读者感受；
- 中文敏感度；
- 人物可信感；
- Flow；
- 不替作者脑补。

### 隔离要求

Blind Reader 不读取：

- Outline；
- PROSE_PACKET；
- Voice Profile；
- Writer 的生成说明；
- 正文原本想表达的语义。

如果条件允许，Blind Reader 使用不同模型或至少独立新上下文。

原因：同一个生成器知道自己为什么写那句话，更容易替自己辩护。

## Role 4：Local Repair

### 任务

根据 `REPAIR_PACKET` 只修指定阅读摩擦。

### 最看重

- 中文局部改写；
- 保持前后声线；
- 不新增事实；
- 不顺手润色健康文本；
- 能接受“少改比多改好”。

### 隔离要求

Repair 不重新读取完整剧情设计。

它只需要：

- 原始正文；
- REPAIR_PACKET；
- 必要的 Active Voice；
- `runtime/LOCAL_REPAIR_CORE.md`。

Repair 的任务不是证明自己比 Writer 会写，而是让一个具体摩擦消失。

## Role 5：Optional Line Reader

不是默认必需。

只在 Blind Reader 指出明确局部语言摩擦，但 Repair 无法判断根因时使用。

任务：定位该处主要属于：

- 中文搭配；
- 指代；
- 句法压缩；
- 节奏；
- 策划语言泄漏；
- 人物口气。

只定位，不全稿清洗。

## 为什么不使用“Writer + Judge 无限循环”

创作质量没有可靠的单一可验证 reward。

如果 Writer 不断针对一个固定 Judge 优化，很容易学会 Judge 的偏好，而不是学会读者。

因此默认只允许：

`Draft → Blind Read → One Local Repair`

真正长期学习信号来自用户接受 / 修改，不来自 AI 自己给自己的分数。

## 解码策略

见 `architecture/DECODING_POLICY.md`。

框架层只规定角色倾向：

- Context Compiler / Voice Analyst：偏稳定；
- Writer：允许适度生成自由度；
- Blind Reader：偏稳定；
- Local Repair：低到中等自由度。

具体 temperature、top-p、min-p 等参数属于模型适配层，不属于正文方法论本体。
