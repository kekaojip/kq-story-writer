# Standalone Prose Engine V1

这是一个**独立的小说正文生成模块设计**。

它暂时不接入 `story-writer-runtime`、Human Writing L2、Main 工作流或任何现有生产链。

目标只有一个：

> 把已经确定的剧情语义，写成读起来像人写的中文小说正文。

它不负责剧情规划，不负责设定管理，不负责伏笔设计，也不负责“去 AI 检测率”。

## 为什么单独做

现有大多数写作框架擅长约束：不能跑剧情、不能泄漏设定、不能解释过头、不能有 AI 痕迹。

这些能让正文少犯错，却不能自动让正文变好看。

本模块只研究正向落字能力：

- 人物当下感
- 叙事距离
- 句子运动
- 自然中文搭配
- 心理如何进入正文
- 对白如何接动作与反应
- 普通句和重点句如何分配
- 段落怎样自然向下一段滑过去
- 如何从用户认可的真实正文中学习声音

## 输入

模块只接受整理后的 `PROSE_PACKET`，不直接吃长篇策划文档。

最小输入：

```yaml
scene_truth:
  must_happen: []
  must_not_happen: []
  pov: ""
  location: ""
  start_state: ""
  end_beat: ""

character_now:
  wants: ""
  knows: []
  notices_first: ""
  immediate_pressure: ""

prose_goal:
  reading_feel: ""
  pace: ""
  distance_bias: "close|mixed|far"

voice_sources:
  approved_samples: []
  previous_accepted_prose: ""
  learned_preferences: []
```

`voice_sources` 可以为空。为空时使用模块自己的自然中文网文基线。

## 输出

```text
draft.md
reader_notes.md
```

- `draft.md`：纯正文。
- `reader_notes.md`：冷读诊断，只标出真正影响阅读的少量问题，不给长篇教学报告。

## 核心流程

```text
PROSE_PACKET
  ↓
Voice Resolve
  ↓
Scene-Now
  ↓
Narrative Distance
  ↓
Paragraph-by-Paragraph Draft
  ↓
Cold Reader (看不到细纲)
  ↓
One Local Revision Pass
  ↓
Final Draft
```

## 四个硬原则

1. **先写正在发生的事，不写对剧情的说明。**
2. **人物怎么注意世界，叙述就怎么移动。**
3. **普通但准确的中文，优先于漂亮但需要翻译的句子。**
4. **只从用户提供、用户认可或正式接受的正文学习声音。原始 AI 草稿永远不能反哺自己。**

## 当前状态

- status: `DESIGN_ONLY`
- production_integration: `NONE`
- modifies_existing_runtime: `NO`
- modifies_human_writing_l2: `NO`
- learns_from_raw_ai_draft: `NO`
