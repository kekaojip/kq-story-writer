# Standalone Prose Pipeline

## 总图

```text
Approved Human Corpus
        │
   DISTILL_VOICE
        │
        ▼
VOICE_PROFILE + Anchor Index
        │
        └──────────────┐
                       │
PROSE_PACKET ──► Context Compiler
                       │
                       ▼
                 WRITER_CONTEXT
                       │
              + WRITE_CORE
              + Active Voice
                       │
                       ▼
                     Draft
                       │
                       ▼
              BLIND_READER_CORE
                       │
              PASS ────┴──── finding
               │               │
               │               ▼
               │          REPAIR_PACKET
               │               │
               │               ▼
               │       LOCAL_REPAIR_CORE
               │               │
               └───────┬───────┘
                       ▼
                  FINAL PROSE
                       │
             human accept / edit
                       │
                LEARN_FROM_EDIT
                       │
                       └──► Voice evidence
```

## 1. 数据面与生成面分离

### 数据面长期保存

- approved human sources；
- accepted project prose；
- significant human corrections；
- Voice Profile；
- anchor index；
- negative drift cases。

### 生成面每次只拿

- 一个 `PROSE_PACKET`；
- Context Compiler 输出的 `WRITER_CONTEXT`；
- `runtime/WRITE_CORE.md`；
- 3-5 条 active voice traits；
- 2-4 个功能相近 anchors；
- 必要的 previous tail。

不把整个语料库、完整大纲或研究文档塞进 Writer。

## 2. 两次压缩

### 第一次：语义压缩

复杂策划 → `PROSE_PACKET` → `WRITER_CONTEXT`。

目的：

- 去掉方法论语言；
- 保留故事硬事实；
- 把注意力收缩到当前场景；
- 防止 Writer 因“知道太多”主动解释。

见 `architecture/CONTEXT_COMPILER.md`。

### 第二次：声音压缩

完整 Voice Profile / corpus → `ACTIVE_VOICE_CONTEXT`。

目的：让 Writer 获得真人声音证据，但不背着整本文风说明书写正文。

## 3. WRITE 路径

### 3.1 Context Compile

输入：`PROSE_PACKET + Voice data + necessary previous prose`。

输出：`WRITER_CONTEXT`。

题材不能自动推导语体。`genre` 与 `register` 分离。

### 3.2 Draft

Writer 默认只看：

- `WRITER_CONTEXT`；
- `runtime/WRITE_CORE.md`；
- `ACTIVE_VOICE_CONTEXT`。

正文按人物注意力和现场反馈推进，不按 outline item 翻译。

### 3.3 Optional Diagnostic Reference

只有出现具体病灶时才按 `SKILL.md` 加载一个对应 reference。

详细 reference 是故障诊断材料，不是第一稿常驻上下文。

### 3.4 Blind Reader

Blind Reader 使用 `runtime/BLIND_READER_CORE.md`。

它看不到设计上下文，只看读感。

默认最多 3 条 finding，硬上限 5 条，并必须指出 `keep`。

### 3.5 Repair Compile

只有真实 finding 才生成 `REPAIR_PACKET`。

把：

- 无关建议；
- 文学偏好；
- 剧情建议；
- 重复 finding

过滤掉。

### 3.6 One Local Repair

Repair 使用 `runtime/LOCAL_REPAIR_CORE.md`。

只改 problem span 及必要邻接，不重新生成整场景。

目标是让具体摩擦消失，而不是“整体更漂亮”。

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

Voice Analyst 可以与 Writer 使用不同模型。

## 5. Anchor Retrieval

召回优先级：

1. 语言功能相似；
2. 互动结构相似；
3. 叙事距离相似；
4. prose mode 相似；
5. Correction / Project Voice；
6. 题材和内容相似。

“同样是修仙场景”不是强匹配。

目标是借鉴：

- 句子运动；
- 信息停点；
- 人物声音进入方式；
- 普通句怎么承担运输。

不是借剧情、句式或比喻。

## 6. LEARN_FROM_EDIT 路径

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

## 7. 失败隔离

### Writer 写坏了

不自动污染 Voice Corpus。

### Blind Reader 判断错了

没有自动改文权，只能提出 finding。

### Repair 写坏了

只能影响一次局部返修，不更新长期 Voice。

### Voice Analyst 过拟合了

Profile 保留 evidence + confidence，可以降级或撤销 trait，不动原始语料。

### 某个模型不适合正文

Model Roles 解耦，可以替换 Writer，而不重做 Voice Corpus 与 PROSE_PACKET。

## 8. 最小可用版本

完全没有母本时也能运行：

```text
PROSE_PACKET
  ↓
Context Compiler
  ↓
WRITE_CORE
  ↓
Blind Reader
  ↓
One Local Repair
```

此时 `voice_confidence=low`。

目标只是不装腔、自然、好读、人物在现场。

有 approved human prose 后，再逐步进入 Voice personalization。

## 9. 模块边界

不进入 Prose Engine：

- 全书大纲管理；
- 商业扫榜；
- 世界状态数据库；
- 伏笔追踪；
- 爽点设计；
- 平台运营；
- AI 检测分数；
- 图片、封面、发布。

它们可以在外部存在，但不能挤进正文运行上下文。
