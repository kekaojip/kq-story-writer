# WRITER TASK

- project: 修仙：我能从未来带回一个结果
- main_project_path: 我能从未来带回一个结果
- chapter: 1
- chapter_title: 我的未来，死在二十七天后
- run_type: FIRST_DRAFT
- platform: 番茄男频
- genre: 玄幻脑洞 / 东方仙侠 / 人生模拟 / 升级流
- pov: 第三人称限知，主要贴林砚
- user_length_request: 用户未单独指定章级字数范围；采用已批准细纲目标
- target_visible_chars: 3200
- wordcount_metric: visible_chars_v1
- delivery_mode: CHECKPOINTED
- delivery_phase: COMPLETE
- heading_literal: # 第一章 我的未来，死在二十七天后
- expected_output:
  - output/current/draft.md
  - output/current/report.json

## MIDPOINT CHECKPOINT
- checkpoint_actual: 1472
- checkpoint_metric: visible_chars_v1
- full_user_band: 2720-3680
- remaining_user_range: 1248-2208
- segment_prefix: output/current/segment.md
- segment_policy: `segment.md` 是冻结正文前缀，必须原样保留；不得为了追字数回改、重写或润色前段。

### front_completed_scope
1. 林砚在黑石矿役调令上看到自己的名字，并确认三日后生效。
2. 核对轮转底册，确认自己的顺位至少被提前一个批次，但没有锁定幕后者。
3. 唐槐作为正常流程参照确认炼气四层可免强制基础矿役；现实修为仍为炼气二层末段。
4. 林砚核算三日时间、3枚灵石、4点贡献、月例与妹妹约0.5灵石药钱，确认修为/资源/人情三条常规路线都不足以翻盘。

### remaining_scope
1. 在常规路线确认无解后，问果第一次开启，只展示本章批准的基础规则：真实未来分支、只能取一果、初始命数1、炼气期跨度最多90日。
2. 林砚进入这条未来，按原命运进入黑石矿；只展开与本次结果选择有关的关键节点。
3. 未来中林砚真实达到炼气四层。
4. 第二十七日发生矿难与地底妖虫混乱，林砚死亡，未来结束。
5. 结算出现多个真实可取结果；由林砚本人比较杠杆，不得由系统推荐。
6. 林砚放弃灵石与模糊矿区情报，唯一选择【结果：炼气四层】。
7. 最终 `draft.md` 必须等于现有 `segment.md` 原文 + 后续正文；章末只写到现实中炼气四层完整成立并被林砚确认，立即停止。

## CURRENT JOB
读取并保留现有 `output/current/segment.md` 作为冻结前缀，只续写 `remaining_scope`。完成整章后输出 `output/current/draft.md` 与 `output/current/report.json`。不得修改已冻结前段，不得新增、删除或重排已经批准的剧情，不写下一章。

## GENRE PROSE CARD
玄幻脑洞为主、东方仙侠为辅。先落现实宗门压力，再让问果规则介入；核心读感是“未来先发生 → 林砚自己比较结果杠杆 → 只取一果 → 现实被撬动”。系统提示短，不写成日志；修仙感落在名册、灵石、修为门槛、功法与宗门规矩，不靠空泛古风词。
