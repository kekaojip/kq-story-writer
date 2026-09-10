# Standalone Prose Engine V1

这是一个**完全独立的中文小说正文生成模块设计**。

当前只存在于：

```text
branch: design/prose-engine-v1
path: standalone/prose-engine-v1/
```

它没有接入 `story-writer-runtime`、Human Writing L2、Main 工作流，也不修改任何现有生产链。

## 唯一目标

> 输入“已经确定要发生什么”，输出“读起来像真人作者写的中文小说正文”。

这里只研究**字怎么写好**。

不研究：

- 选题；
- 大纲；
- 爽点设计；
- 世界观；
- Tracking；
- 商业运营；
- AI 检测率。

## 为什么重新单独做

旧式 AI 小说系统很容易把精力放在：

- 禁词；
- 不能跑剧情；
- 不能解释过头；
- 不能用破折号；
- 各类 AI pattern detector。

这些是护栏，能让稿子少犯病，却不能告诉模型“一个真人小说作者在这里到底会怎么落字”。

Prose Engine V1 的核心方向改成**正向正文生成**：

1. 真人 Voice 是声音证据。
2. 人物注意力决定叙述顺序。
3. 叙事距离必须随场景移动。
4. 中文先服从母语自然搭配。
5. 句子和段落靠信息运动形成节奏，不靠标点技巧。
6. 对白是人物做事，不是作者发设定。
7. 大量普通句负责运输，重点句才有力量。
8. Blind Reader 只看真实阅读体验。
9. 长期学习只来自用户接受和修改，不来自 AI 自己的草稿。

## 三个运行模式

### WRITE

`PROSE_PACKET → Voice Resolve → Lived Draft → Blind Reader → One Repair → Final Prose`

只写正文。

### DISTILL_VOICE

`Approved Human Prose → Contrastive Distillation → VOICE_PROFILE + Anchor Index`

只学习真人声音。

### LEARN_FROM_EDIT

`AI Before + Human After → Significant Diff → Voice Update Proposal`

只从真实修改学习。

详细见：

`architecture/RUN_MODES.md`

## 核心架构

```text
Approved Human Corpus
       │
       ▼
DISTILL_VOICE ──► VOICE_PROFILE + Anchor Index
                         │
                         ▼
PROSE_PACKET ──► Scene Frame ──► Voice Resolve
                                  │
                                  ▼
                              Lived Draft
                                  │
                                  ▼
                             Blind Reader
                                  │
                                  ▼
                           One Local Repair
                                  │
                                  ▼
                              FINAL PROSE
                                  │
                      human accept / edit
                                  │
                                  ▼
                           LEARN_FROM_EDIT
```

完整图见：

`architecture/PIPELINE.md`

## 关键设计

### 1. Truth 与 Voice 分离

`PROSE_PACKET` 负责“不能写错什么”。

`VOICE_PROFILE` 负责“这种文字通常怎么说”。

大纲措辞、策划术语永远不是 Voice。

### 2. Voice 三层证据

优先级：

```text
Correction Voice
    > Project Voice
    > Author Voice
```

- Correction Voice：用户亲手改过并认可的正文。
- Project Voice：本项目正式接受正文。
- Author Voice：用户自己的作品或明确批准的真人母本。

Raw AI draft 永远不能成为正向声音源。

### 3. 不是只给“风格总结”，还要给真人 Anchor

每次生成只取：

- 3-5 条 active voice traits；
- 2-4 个功能相近的真人 prose anchors；
- 0-2 个反复 drift warning。

Anchor 优先按“当前场景要完成什么语言功能”召回，不按题材专名硬匹配。

### 4. Contrastive Voice Distillation

不直接对母本说“总结一下文风”。

默认流程：

```text
Human Sample
  → Semantic Skeleton
  → 同语义 Neutral Baseline
  → Human vs Baseline Contrast
  → Claim + Evidence
  → 跨样本聚合
  → Domain / Character / Scene-Type Filter
  → Voice Profile
```

这样更容易把“作者怎么写”从“这段发生了什么”中剥离出来。

### 5. 人物意识优先于作者逻辑

正文不是：

`背景 → 原因 → 风险 → 方案 → 结论`

默认跟随：

`刺激 → 当下判断/反应 → 动作/对白 → 现实反馈`

但每一拍不要求全部写完。

人物可以想一半、先做事、被打断、回头再判断。

### 6. 叙事距离会动

AI 很容易整章待在安全的中间距离。

本模块明确允许：

- 决定、危险、欲望、羞耻时靠近人物；
- 转场、时间经过、重复劳动时拉远；
- close POV 时让人物词汇进入旁白，少用“他意识到”做中介。

### 7. 中文单独有底座

英文 fiction craft 不能自动保证中文自然。

`Chinese Prose Base` 单独约束：

- 现代书面白话；
- 常见中文搭配；
- 允许自然的“了、就、还、又、却”等语气/连接颗粒；
- 不为题材感做旧普通句；
- 不把自然中文压成电报；
- 口语化不等于聊天化。

### 8. 句子节奏不是短句率

模块不使用：

- 短句 X%；
- 对白 X%；
- 比喻每千字 X 次；
- 每段 X 字。

分析可以统计，生成不按配额施工。

句子运动来自：

- 当前信息工作；
- 注意对象变化；
- 叙事距离；
- 动作与判断接力；
- 长短自然起伏。

### 9. Blind Reader 不知道作者意图

Blind Reader 只能看正文和目标读者。

它判断：

- Flow；
- Presence；
- Character Mind；
- Language Pleasure；
- Pull。

必须同时记录 `keep`，避免返修把已经好的部分洗掉。

只允许一次局部 repair，不无限优化一个 AI Judge。

## 文件结构

```text
standalone/prose-engine-v1/
├── README.md
├── SKILL.md
├── architecture/
│   ├── MODEL_ROLES.md
│   ├── PIPELINE.md
│   └── RUN_MODES.md
├── specs/
│   ├── PROSE_PACKET.md
│   ├── PROSE_QUALITY.md
│   ├── VOICE_CORPUS.md
│   └── VOICE_PROFILE.md
├── references/
│   ├── chinese-prose-base.md
│   ├── sentence-and-paragraph-motion.md
│   ├── scene-writing.md
│   ├── character-consciousness.md
│   ├── dialogue-and-handoffs.md
│   ├── voice-system.md
│   ├── voice-distillation.md
│   ├── anchor-retrieval.md
│   ├── prose-generation-loop.md
│   ├── cold-reader.md
│   └── learning-loop.md
└── research/
    └── DESIGN_DECISIONS.md
```

`research/` 永远不是运行时上下文。

## 模型角色

不写死一个模型。

允许分别选择：

- **Prose Writer**：看实际中文小说落字能力；
- **Voice Analyst**：看细读、比较、归纳能力；
- **Blind Reader**：最好独立模型或独立新上下文；
- 可选 Line Reader：只处理明确局部语言摩擦。

“最聪明的推理模型”不自动等于“最好的小说正文模型”。

## 当前状态

```yaml
status: DESIGN_ONLY
production_integration: NONE
modifies_story_writer_runtime: NO
modifies_human_writing_l2: NO
modifies_main_workflow: NO
learns_from_raw_ai_draft: NO
ai_detection_as_goal: NO
```

下一阶段只有在模块本身设计成熟以后，才讨论如何接到任何外部生产系统。