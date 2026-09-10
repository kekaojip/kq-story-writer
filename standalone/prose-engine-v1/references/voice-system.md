# Voice System

## 目标

Voice 不是“幽默、克制、短句、网文感”几个形容词。

Voice 是作者在不同场景里反复做出的**语言选择**：句子怎么起、注意力怎么移、心理怎么进、对白怎么接、哪里故意写得普通。

本系统只从经过批准的正文证据中建立 Voice。

完整数据契约见：

- `specs/VOICE_CORPUS.md`
- `specs/VOICE_PROFILE.md`
- `references/voice-distillation.md`
- `references/anchor-retrieval.md`

## 三层声音

### 1. Author Voice

跨项目、变化慢。

来自：

- 用户自己的既有作品；
- 用户明确批准的真人作者样本；
- 用户授权作为长期语言参考的母本。

回答：这个用户总体喜欢什么样的中文小说声音。

### 2. Project Voice

当前作品内部形成的声音。

只从正式接受正文积累。

回答：同一套底层偏好进入这本书以后，具体怎样变化。

### 3. Correction Voice

用户对 AI 正文做出的明确修改。

这是最高价值证据。

回答：模型当前最容易写偏在哪里，用户真正会怎样落字。

冲突优先级：

`Correction Voice > Project Voice > Author Voice`

但先判断 scope。战斗场景习惯不应自动覆盖所有场景，某个角色的说话方式也不等于全书旁白。

## Voice 的七个核心维度

不是每个项目都必须填满。文本决定哪些维度真正稳定。

### Sentence Motion

- 动作、判断、感知、对白谁更常先出现；
- 一个信息通常几句落完；
- 长短句怎么随场景变化；
- 句间关系显式说还是靠语序承接。

### Narrative Distance

- 默认离人物多近；
- 什么情境会拉近；
- 什么情境会拉远；
- 是否常用自由间接式人物判断。

### Interiority

- 心理多深；
- 直接判断、动作携带、内心展开各自什么时候出现；
- 一次念头通常处理到哪一层就停。

### Vocabulary & Collocation

- 常用普通动词；
- 抽象名词与具体词的倾向；
- 功能词、连接词、题材词如何使用；
- 哪些自然搭配反复出现。

重点学普通词，不是收集华丽词。

### Dialogue Handoff

- 台词后接下一句、动作、心理还是留白；
- 说话标签显眼度；
- 熟人共享信息省略程度；
- 冲突、礼貌、上下级关系怎样改变句子。

### Paragraph Rhythm

- 什么注意变化触发换段；
- 哪些重点句会独立；
- 普通段落怎样把读者送到下一拍。

### Plainness

专门记录作者**哪里没有用力写**。

这是 Voice 系统必须保存的一维。

只学习显眼的特色句，会让模型误以为“作者风格 = 每句话都要有特色”。真人正文真正稳定的底色往往藏在大量普通句里。

## 蒸馏方法

不要直接让模型读一章后总结“文风”。

默认使用 `voice-distillation.md` 的 contrastive 方法：

1. 按场景功能切真人样本；
2. 抽出 Semantic Skeleton；
3. 建立同语义 Neutral Baseline；
4. 比较 Human Sample 与 Baseline；
5. 只保留可迁移的语言差异；
6. 跨样本聚合；
7. 做 domain / character / scene-type 过滤；
8. 形成 Claim + Evidence 的 Voice Profile。

这样能减少把剧情内容、题材词和偶然金句误当成文风。

## 生成时不加载整套档案

完整 Voice Profile 可以保存较多证据，但每次正文生成只激活：

- 3-5 条当前 trait；
- 2-4 个当前功能相近 anchor；
- 0-2 条反复出现的 drift warning。

超过这个规模容易退化成 checklist 写作。

## Anchor 的价值

抽象 trait 只告诉 Writer 方向。

Anchor 告诉 Writer：这种场景里，真人正文的**运动方式**是什么。

召回优先：

1. 功能相似；
2. prose mode 相似；
3. project / correction 相关；
4. narrative distance 相似；
5. 内容与题材相似。

学习运动，不复制词面。

## 学习边界

### 正向来源

- 用户明确批准的真人样本；
- 用户自己的作品；
- 用户亲手修改并确认的版本；
- 当前项目正式接受正文。

### 绝不成为正向来源

- 未审核 AI 草稿；
- 被拒绝稿；
- detector clean；
- AI 自己给自己的 PASS；
- outline / planning / review 的措辞。

AI 草稿只能进入 Negative Drift Corpus，或者和用户修改版组成 before/after diff。

## 防过拟合

Voice 的目标不是逐句模仿某个作者。

必须避免：

- 复制独特比喻；
- 复制专名与桥段；
- 把一次出现变成固定习惯；
- 把统计比例直接当生成配额；
- 单一母本压过用户后续修改；
- 为了“像”而牺牲当前人物、场景和自然中文。

最终标准只有一个：

> 用户能认出声音方向，但读者不会感觉正文在表演“模仿文风”。