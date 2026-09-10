# REPAIR_PACKET Contract

## 目的

把 Blind Reader 的读感 finding 编译成一次**局部返修任务**。

Repair 不是第二次写作，不允许借机“整体润色”。

## 输入格式

```yaml
REPAIR_PACKET:
  immutable:
    story_facts: []
    knowledge_boundary: []
    end_state: ""
    stop_point: ""

  keep:
    - "已经成立、禁止破坏的读感或声音"

  findings:
    - id: BR1
      location: ""
      impact: flow | presence | character_mind | natural_chinese | pull
      reader_effect: ""
      problem_span: ""
      minimal_direction: ""

  repair_budget:
    max_passes: 1
    scope: local_only
```

## 编译规则

只把真正影响阅读的 finding 放进 Repair Packet。

Blind Reader 的个人偏好、文学建议、剧情建议全部丢弃。

同一位置多个 finding 如果本质相同，合并成一条。

## 局部范围

默认每个 finding 只允许修改：

- 问题句；
- 必要时前后 1-2 段；
- 为保持衔接所需的最小邻接文本。

除非问题本身跨越多个段落，否则不得整场景重写。

## Repair 不可改变

- 已批准事件；
- 人物选择；
- 因果；
- 数字、能力、物品状态；
- 人物知道/不知道什么；
- 场景结束状态；
- stop point；
- 已经成立的 `keep`。

## Repair 的成功定义

不是“更漂亮”。

是：

> 原先那个具体阅读摩擦消失了，同时周围健康正文基本没动。

如果修复一个病句需要重写半章，优先判定 Repair Packet 过宽或原问题被误诊。
