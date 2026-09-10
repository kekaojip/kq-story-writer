# Standalone Prose Pipeline

## 总图

```text
                 ┌──────────────────────────┐
                 │   Approved Human Corpus  │
                 └────────────┬─────────────┘
                              │
                       DISTILL_VOICE
                              │
                              ▼
                     ┌────────────────┐
                     │ VOICE_PROFILE  │
                     │ + Anchor Index │
                     └───────┬────────┘
                             │
PROSE_PACKET ──► Semantic Wash
                     │
                     ▼
                 Scene Frame
                     │
                     ▼
                Voice Resolve ◄───────────────┐
                     │                         │
                     ▼                         │
                 Lived Draft                   │
                     │                         │
              Local Distance/Voice             │
                     │                         │
                     ▼                         │
               Continuity Read                 │
                     │                         │
                     ▼                         │
                 Blind Reader                  │
                     │                         │
                     ▼                         │
                One Local Repair               │
                     │                         │
                     ▼                         │
                  FINAL PROSE                  │
                     │                         │
        human accept / human edit              │
                     │                         │
             LEARN_FROM_EDIT ──────────────────┘
```

## 1. 数据面与生成面分离

### 数据面

长期保存：

- approved human sources；
- accepted project prose；
- significant human corrections；
- Voice Profile；
- anchor index；
- negative drift cases。

### 生成面

每次只拿：

- 一个 PROSE_PACKET；
- 3-5 条 active voice traits；
- 2-4 个 anchors；
- 必要的 Chinese Prose Base / craft references。

不把整个语料库塞进 Writer。

## 2. 为什么要两次“压缩”

### 第一次：语义压缩

复杂策划 → PROSE_PACKET。

目的：让 Writer 不继承上游方法论语言。

### 第二次：声音压缩

完整 Voice Profile / corpus → active traits + anchors。

目的：让 Writer 不背着一整本风格说明书写正文。

正文模型上下文里应该主要是：

- 当前场景；
- 当前人物；
- 少量声音证据。

## 3. WRITE 路径

### 3.1 Semantic Wash

把任何上游标签还原成事实。

### 3.2 Scene Frame

锁定“现在”：人物从哪里开始，第一注意对象是什么，眼下要什么。

### 3.3 Voice Resolve

从 Voice Profile 选择当前有用的 trait；从 Corpus 召回功能相近 anchor。

### 3.4 Draft in Micro-scenes

每个微场景围绕一个注意对象或互动拍。

不按固定字数，不按 outline item。

### 3.5 Local Craft Pass

只看：

- 叙事距离；
- 中文搭配；
- 句子/段落运动；
- 对白接力；
- Voice 明显偏航。

健康段落不改。

### 3.6 Blind Reader

完全隔离设计上下文，只看读感。

### 3.7 One Repair

只修真正影响阅读的问题。

## 4. DISTILL_VOICE 路径

```text
Approved Source
   ↓
Functional Segmentation
   ↓
Semantic Skeleton
   ↓
Neutral Baseline
   ↓
Contrastive Analysis
   ↓
Claim + Evidence
   ↓
Cross-sample Clustering
   ↓
Scope / Domain Filter
   ↓
VOICE_PROFILE + Anchor Index
```

这个过程可以使用与 Writer 不同的模型。

## 5. LEARN_FROM_EDIT 路径

```text
AI Before + Human After
   ↓
Significance Filter
   ↓
Language-choice Diff
   ↓
Scope Guess
   ↓
Trait Proposal
   ↓
Evidence Accumulation / Explicit Approval
   ↓
VOICE_PROFILE update
```

没有人类 after，就没有正向学习。

## 6. 失败隔离

### Writer 写坏了

不自动污染 Voice Corpus。

### Blind Reader 判断错了

没有自动改文权，只能提出局部 finding。

### Voice Analyst 过拟合了

Profile 中保留 evidence + confidence，可以降级/撤销 trait，而不是修改原始语料。

### 某个模型不适合正文

Model Roles 解耦，可以替换 Writer，不重做 Voice Corpus 和 PROSE_PACKET。

## 7. 最小可用版本

即使完全没有母本，模块也能运行：

```text
PROSE_PACKET
  + Chinese Prose Base
  + Scene / Consciousness / Dialogue / Motion
  → WRITE
  → Blind Reader
  → One Repair
```

此时 `voice_confidence=low`，目标是自然、好读、有现场感，不假装拥有独特作者声音。

有真人母本后，再逐步进入真正 Voice personalization。

## 8. 不进入这个模块的东西

- 全书大纲；
- 商业扫榜；
- 世界状态数据库；
- 伏笔追踪；
- 爽点设计；
- 平台运营；
- AI 检测分数；
- 图片、封面、发布。

它们都可以在外部存在，但 Prose Engine 不承担。

这条边界必须一直守住，否则正文模块会再次膨胀成“什么都会一点、落字依旧不好”的总工作流。