# Prose Engine V1 · Design Decisions

> 这是设计依据，不是运行时 prompt。Prose Engine 生成正文时不读取本文件。

## D1. 不再把“去 AI”当正文生成器

### 观察

大量 anti-slop / humanizer 工具能删除明显模板、破折号、总结句和空泛表达，但不能凭空提供稳定作者声音。

中文社区也存在“humanizer 后检测率更高 / 文字更怪”的反馈，说明单纯后处理不是可靠主路径。

### 决策

- Anti-AI 只能做诊断层。
- 正文必须有独立 Positive Prose Generation。
- 不使用“完整 AI 初稿 → 全文 humanize → 全文润色”的默认链。

## D2. 人类正文必须成为声音证据，不只是几条形容词

### 研究依据

`Whose story is it? Personalizing story generation by inferring author styles` 使用 Author Writing Sheet，从多篇真人作品中提取 Claim + Evidence，个性化故事在风格捕获上显著优于非个性化 baseline。

`Catch Me If You Can? Not Yet` 说明少量 few-shot 样本能带来改善，但模型仍容易退回平均、generic tone；简单增加 demonstrations 收益有限。

`Towards Human-Level Book-Writing Capability` 的核心做法之一，是让原始人类小说正文继续作为最终监督目标，而不是把 AI 生成正文当成训练真值。

### 决策

Voice System 必须同时保存：

- 归纳出的 trait；
- trait 的证据来源；
- 可按当前场景召回的少量真人 anchor。

不能只保存“短句、克制、节奏快”。

## D3. Voice 需要分层，而不是一张全书风格卡

### 工程参考

2389 Research `word-compiler` 的 personalization layer 分离：

1. Author Voice；
2. 用户显式修改形成的 CIPHER preferences；
3. 当前 Project Voice。

并在生成时压缩成小型 injection。

### 决策

本模块采用：

`Correction Voice > Project Voice > Author Voice`

但先判断 scope，避免当前场景习惯错误覆盖全局声音。

## D4. 不用巨型固定风格 taxonomy 驱动生成

### 工程参考

`creative-writing-skills` 的 style analysis 强调：先看当前文本哪些维度真的变化，再决定怎么拆；每个 style file 使用 Principle + 少量 Representative Examples，并明确警告 exhaustive checklist 会使写作机械化。

中文开源项目常见把文风拆成句长比例、感官比例、对白比例、比喻密度等统计维度。这些适合分析和诊断，但直接作为生成配额会反过来制造模板。

### 决策

- Voice Profile 可以统计，但 Writer 只收到 3-5 条 active traits。
- 每次只召回 2-4 个功能相近 anchor。
- 不默认使用短句率、对白率、比喻/千字等硬指标生成正文。

## D5. 叙事距离是“好不好看”的核心变量

### 工程参考

`creative-writing-skills/resources/prose-writing.md` 明确指出：默认 AI prose 常停在平坦的中间 psychic distance。

这与我们的失败样本高度一致：人物似乎有内心，但叙述始终是作者替他总结和分析。

### 决策

Prose Engine 把 Narrative Distance 变成第一稿生成变量：

- 决策 / 危险 / 羞耻 / 欲望时允许拉近；
- 转场 / 时间压缩 / 物流时拉远；
- 靠近 POV 时优先 free-indirect-like 直接判断，而不是不断写“他意识到”。

## D6. 按注意力和微因果生成，不按提纲条目翻译

### 观察

通用助手模型擅长把信息整理成结构化答案。

小说正文如果直接继承这个能力，就会出现：

- 先说 A、再说 B、最后 C；
- 修为 / 资源 / 人情 / 风险逐项盘点；
- 每个刺激被完整推演成原因、方案、结论。

### 决策

正文的局部推进单位改为：

`刺激 → 当前反应/判断 → 动作/对白 → 现实反馈`

但不要求四步齐全。

核心是人物的注意力顺序，不是策划逻辑顺序。

## D7. 中文需要独立语言底座

### 观察

英文 fiction craft 能解决 POV、距离、场景，但无法直接保证中文词组搭配自然。

中文 AI 常见问题包括：

- 普通动作被小说化重组；
- 抽象名词偏多；
- 过度删除“了、就、还、又”等自然连接；
- 题材词污染普通叙述；
- 为了短促把句子压成电报。

### 决策

独立建立 `Chinese Prose Base`：

- 现代书面白话默认；
- 常见中文搭配优先；
- 保留必要功能词；
- 普通句承担运输；
- 口语化不等于聊天记录。

## D8. Cold Reader 看体验，不做第二个规则审查器

### 工程参考

`creative-writing-skills` 的 reader simulation 把阅读体验拆成 transportation、aesthetic、social simulation、curiosity、flow，而不是只检查技法。

### 决策

Blind Reader 只看正文，不看大纲和作者意图。

重点评估：

- Flow；
- Presence；
- Character Mind；
- Language Pleasure；
- Pull。

并且必须记录 `keep`，防止返修把已经成立的部分洗掉。

## D9. 只从用户认可决策学习

### 工程参考

Writer's Loop 的核心规则：`Learn from user decisions, not from raw AI drafts.`

Word Compiler 也将用户 significant edits 单独作为最高信号之一。

### 决策

- 原始 AI draft 永不进入正向 Voice Memory。
- 用户修改 diff 是最高价值数据。
- 先过滤标点/错字/单次事实，再提取稳定写法。
- 同类修改反复出现或用户明确认可后才升级。

## D10. 专用创作模型与通用助手模型要分开看

### 研究依据

`Towards Human-Level Book-Writing Capability` 指出通用 assistant alignment 与小说需求存在目标错配，并报告专门创作训练能显著改变正文表现。

### 决策

Prose Engine 设计必须允许更换底层 Writer model。

模块不假设“最聪明的通用推理模型就是最好的正文模型”。

未来可以独立比较：

- frontier assistant model；
- Chinese web-fiction fine-tune；
- local novel model。

但模型选择不写死进框架。