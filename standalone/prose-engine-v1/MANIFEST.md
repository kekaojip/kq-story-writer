# Prose Engine V1 Manifest

## 状态

```yaml
branch: design/prose-engine-v1
status: DESIGN_ONLY
production_integration: NONE
production_main_modified_by_this_module: NO
```

## Runtime Entry

- `SKILL.md`：轻量路由器。
- `runtime/WRITE_CORE.md`：WRITE 第一稿最小正文核心，只写不审。
- `runtime/BLIND_READER_CORE.md`：独立盲读体验传感器。
- `runtime/LOCAL_REPAIR_CORE.md`：一次局部返修核心。

正常 WRITE 不默认加载全部 references。

## Architecture

- `architecture/PIPELINE.md`：端到端数据流与生成流。
- `architecture/CONTEXT_COMPILER.md`：把剧情语义与 Voice 编译成最小 Writer 上下文。
- `architecture/RUN_MODES.md`：WRITE / DISTILL_VOICE / LEARN_FROM_EDIT。
- `architecture/MODEL_ROLES.md`：Writer / Voice Analyst / Blind Reader / Local Repair 分工。
- `architecture/DECODING_POLICY.md`：模型无关的正文采样方向；具体参数留在模型适配层。

## Specs

- `specs/PROSE_PACKET.md`：独立正文输入协议，明确 `genre != register`。
- `specs/PROSE_QUALITY.md`：正文质量验收定义。
- `specs/REPAIR_PACKET.md`：盲读 finding 到局部返修的最小任务协议。
- `specs/VOICE_CORPUS.md`：approved prose 语料、证据强度与 anchor 存储协议。
- `specs/VOICE_PROFILE.md`：长期 Voice Profile。
- `specs/ACTIVE_VOICE_CONTEXT.md`：每次 Writer 真正加载的紧凑声音上下文。

## Positive Prose References

- `references/chinese-prose-base.md`：自然现代中文底座。
- `references/sentence-and-paragraph-motion.md`：句子与段落运动。
- `references/scene-writing.md`：场景当前拍推进。
- `references/detail-and-compression.md`：细节选择、展开与压缩。
- `references/character-consciousness.md`：人物意识与叙事距离。
- `references/dialogue-and-handoffs.md`：对白互动与接力。
- `references/prose-generation-loop.md`：正向生成详细说明，仅诊断时使用。

## Voice References

- `references/voice-system.md`：三层 Voice 总协议。
- `references/voice-distillation.md`：contrastive 文风蒸馏。
- `references/anchor-retrieval.md`：功能型真人 anchor 召回。
- `references/voice-validation.md`：close reading + stylometry 旁证。
- `references/learning-loop.md`：从用户修改学习。

## Reader Reference

- `references/cold-reader.md`：Blind Reader 详细设计说明。

运行时默认使用更短的 `runtime/BLIND_READER_CORE.md`。

## Research Only

运行时禁止加载：

- `research/DESIGN_DECISIONS.md`
- `research/EVALUATION_AND_DIVERSITY.md`

这些文件只保存设计依据。

## WRITE 默认上下文

第一稿 Writer 只给：

1. Context Compiler 生成的 `WRITER_CONTEXT`；
2. `runtime/WRITE_CORE.md`；
3. `ACTIVE_VOICE_CONTEXT`（存在时）；
4. 必要的上一段正式正文尾部。

第一稿阶段不模拟 Reviewer，不做语言评分。

不默认给：

- 完整大纲；
- research；
- 全量 Voice Profile；
- 整本母本；
- Review 报告；
- 被拒绝 AI 草稿。

专项 reference 只有命中具体问题才按 `SKILL.md` 路由读取。

## Repair 默认上下文

Repair 只给：

1. 原始正文；
2. `REPAIR_PACKET`；
3. `runtime/LOCAL_REPAIR_CORE.md`；
4. 必要时少量 Active Voice。

最多一轮，局部修改，保护 `keep`。

## Voice Evidence Hierarchy

默认：

```text
user_correction > user_written / human_reference > accepted_project
```

`accepted_project` 主要服务当前项目连续性，不能单独创建新的 global Voice trait。

## 当前核心设计判断

- 正向正文生成优先于去 AI 后处理。
- 写与审分离，第一稿只写，Blind Reader 独立判断。
- 人物注意力优先于策划逻辑顺序。
- 叙事距离是第一稿变量，不是审稿后补丁。
- `genre` 与 `register` 分离，题材不能自动把中文古老化。
- 中文常见搭配优先于“小说化”重组。
- 普通句是正常正文的重要组成。
- Voice 使用真人证据 + 功能型 anchor，不靠形容词列表。
- Anchor 按语言功能优先召回，题材相似最后考虑。
- Correction Voice > Project Voice > Author Voice；同层仍受 evidence strength 约束。
- Raw AI draft 永远不成为正向 Voice。
- 分析统计可以验证 Voice，不直接控制生成比例。
- Blind Reader 是体验传感器，不是文学法官，也没有改稿权。
- Repair 只消除具体摩擦，不重新写一篇“更漂亮”的版本。
- 默认最多一次局部 repair，不做无限 Judge 优化。
- Writer 可使用适度随机采样，具体解码参数按模型独立适配。
- 任何模型都可替换，框架不写死模型名。
