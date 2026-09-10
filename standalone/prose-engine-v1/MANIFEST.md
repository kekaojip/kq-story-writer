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
- `runtime/WRITE_CORE.md`：WRITE 模式默认正向正文核心。

正常 WRITE 不默认加载所有 references。

## Architecture

- `architecture/PIPELINE.md`：端到端数据流与生成流。
- `architecture/RUN_MODES.md`：WRITE / DISTILL_VOICE / LEARN_FROM_EDIT。
- `architecture/MODEL_ROLES.md`：Writer / Voice Analyst / Blind Reader 分工。

## Specs

- `specs/PROSE_PACKET.md`：独立正文输入协议。
- `specs/PROSE_QUALITY.md`：正文质量验收定义。
- `specs/VOICE_CORPUS.md`：approved prose 语料与 anchor 存储协议。
- `specs/VOICE_PROFILE.md`：长期 Voice Profile。
- `specs/ACTIVE_VOICE_CONTEXT.md`：每次 Writer 真正加载的紧凑声音上下文。

## Positive Prose References

- `references/chinese-prose-base.md`：自然现代中文底座。
- `references/sentence-and-paragraph-motion.md`：句子与段落运动。
- `references/scene-writing.md`：场景当前拍推进。
- `references/detail-and-compression.md`：细节选择、展开与压缩。
- `references/character-consciousness.md`：人物意识与叙事距离。
- `references/dialogue-and-handoffs.md`：对白互动与接力。
- `references/prose-generation-loop.md`：正向生成 passes。

## Voice References

- `references/voice-system.md`：三层 Voice 总协议。
- `references/voice-distillation.md`：contrastive 文风蒸馏。
- `references/anchor-retrieval.md`：功能型真人 anchor 召回。
- `references/voice-validation.md`：close reading + stylometry 旁证。
- `references/learning-loop.md`：从用户修改学习。

## Reader

- `references/cold-reader.md`：Blind Reader 体验评估。

## Research Only

运行时禁止加载：

- `research/DESIGN_DECISIONS.md`
- `research/EVALUATION_AND_DIVERSITY.md`

这些文件只保存设计依据。

## WRITE 默认上下文预算

正常正文生成只给 Writer：

1. `PROSE_PACKET`
2. `runtime/WRITE_CORE.md`
3. `ACTIVE_VOICE_CONTEXT`（存在时）
4. 必要的上一段正式正文上下文（由调用者提供）

专项 reference 只有命中具体问题才按 `SKILL.md` 路由读取。

## 当前核心设计判断

- 正向正文生成优先于去 AI 后处理。
- 人物注意力优先于策划逻辑顺序。
- 叙事距离是第一稿变量，不是审稿后补丁。
- 中文常见搭配优先于“小说化”重组。
- 普通句是正常正文的重要组成。
- Voice 使用真人证据 + 功能型 anchor，不靠形容词列表。
- Correction Voice > Project Voice > Author Voice。
- Raw AI draft 永远不成为正向 Voice。
- 分析统计可以验证 Voice，不直接控制生成比例。
- Blind Reader 是体验传感器，不是文学法官。
- 默认最多一次局部 repair，不做无限 Judge 优化。
- 任何模型都可替换，框架不写死模型名。