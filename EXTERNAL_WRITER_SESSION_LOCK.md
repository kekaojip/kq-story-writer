# EXTERNAL_WRITER_SESSION_LOCK — 独立 Writer 会话硬锁

状态：ENFORCED
适用仓库：`kekaojip/kq-story-writer`

## 最高规则

本仓库只能由**独立 External Writer AI 会话**执行正文任务。

本会话不得同时承担 Main / Planner / Reviewer / Tracking 职责。

正确拓扑：

```text
另一个 AI 会话（Main）
→ 已经把完整任务发布到本仓 input/current/
→ KQ 把 Writer 提示词复制到当前独立会话
→ 当前会话只读本仓并生成 output/current/
→ 停止
→ KQ 回 Main 会话继续审稿
```

---

## 1. 仓库读取边界

当前 Writer 会话只允许读取：

`kekaojip/kq-story-writer`

禁止读取或检索：

- `kekaojip/kq-story-test`
- `kekaojip/kq-story`
- 任何其他小说主仓、规划仓、拆文仓
- 聊天中未发布到 `input/current/` 的未来剧情或旧版本正文

即使当前 AI 拥有 GitHub 权限，也不得跨仓补资料。

Writer 的全部事实输入只能来自当前 Writer 仓的 `input/current/`。

---

## 2. 角色冲突硬阻塞

如果当前用户提示词出现以下任一种情况：

- 要求“同时读取两个仓库”；
- 要求读取 `kq-story-test` 后再写正文；
- 要求当前会话从零规划小说并继续生成正文；
- 要求当前会话承担 Main + Writer 两个角色；
- 要求当前会话自己生成 Workspace 再自己写；
- 要求当前会话修改 Tracking / 主仓正式正文 / 大纲；

则不得继续正文生成。

必须停止并返回：

`WRITER_SESSION_ROLE_CONFLICT`

并说明：请先在独立 Main 会话完成规划与 Workspace 发布，再把只指向 `kq-story-writer` 的 Writer 提示词发到当前会话。

---

## 3. 可执行条件

只有同时满足以下条件才允许写：

1. 当前任务只指向 `kq-story-writer`；
2. `input/current/00_TASK.md` 存在；
3. `input/current/HANDOFF_STATE.json` 存在；
4. HANDOFF 状态允许当前执行；
5. `expected_output` 明确；
6. 所需 input 已由 Main 发布；
7. 不需要读取主仓才能理解任务。

缺任一项：停止并报告缺口，不自行补规划。

---

## 4. Writer 完成后的强制停止

Writer 只生成 HANDOFF 要求的 `output/current/` 文件。

完成后：

- 不审稿；
- 不运行主仓 `story-review`；
- 不更新 Tracking；
- 不收编正式正文；
- 不规划下一章；
- 不读取主仓查看后续；
- 不自行进入下一阶段。

用户可见回复只需：

```text
WRITER_DONE
生成文件：<实际 output/current 文件名>
请回到 Main 工作流窗口继续。
```

---

## 5. CHECKPOINTED 同样要求跨会话中转

若当前是 `CHECKPOINTED / FRONT`：

- 只生成 `segment.md`；
- 然后停止；
- KQ 回 Main 会话做 midpoint checkpoint。

Main 更新 HANDOFF 为 `CHECKPOINTED / COMPLETE` 后，KQ 再回到 Writer 会话或新开独立 Writer 会话继续。

Writer 不得自己计算 Main 的 checkpoint 后接着写 COMPLETE。

因此完整章节可能发生多次人工中转，这是设计要求，不是失败。

---

## 6. 冲突优先级

本硬锁高于本仓任何允许单会话自动串行完成 Main + Writer 的旧说明。

它不改变 Writer 的正文能力，只确保正文能力永远由独立 Writer AI 会话执行。
