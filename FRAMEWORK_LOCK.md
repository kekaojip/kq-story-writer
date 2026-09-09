# FRAMEWORK LOCK — Writer Runtime 框架保护协议

状态：LOCKED
所有者：KQ
适用仓库：`kekaojip/kq-story-writer`

## 最高规则

除非 KQ 在当前任务中明确批准，否则任何 Agent、模型、脚本或自动化都不得删除、覆盖、改名、移动、重构、职责迁移或实质替换 Writer Runtime 框架。

允许在现有框架基础上做增量优化，但必须遵守：**新增优先，原件不动；旁路优先，替换需授权。**

## 受保护框架

默认受保护：

- `skills/story-writer-runtime/**` 下所有当前已存在文件与目录；
- `START_HERE.md`；
- `README.md`；
- `UPSTREAM.md`；
- `docs/**` 下所有当前已存在的生产协议与拆分文档；
- `output/current/OUTPUT_CONTRACT.md`；
- Writer Runtime 的职责边界、输入输出协议和 External Writer Bridge V1 交接规则；
- 以后明确标记为 `LOCKED` 的框架文件。

`input/current/`、`output/current/draft*.md`、`output/current/report*.json`、`archive/` 中的任务数据与章节产物属于运行数据，不属于框架本体，可按生产流程创建、替换、归档或清理。

## 未经批准禁止的操作

1. 修改受保护文件已有正文、规则、接口或职责。
2. 删除、改名、移动受保护文件。
3. 用新 Skill、新 Agent、新脚本绕过或替代现有 Writer Runtime。
4. 把规划、Tracking、世界真相维护等主仓库职责迁入 Writer。
5. 把正文语言执行职责迁回主模型，绕过 Writer Bridge。
6. 批量同步 upstream 时覆盖 KQ 已锁定的本地运行框架。
7. 以“清理、重构、优化、升级、修复”为理由改变框架行为而未取得 KQ 明确许可。

## 默认允许的操作

在不改变现有框架行为的前提下，可以：

- 新增独立 reference、检查器、适配器、文档、实验工具；
- 发布新的 `input/current/` 任务；
- Writer 生成与返修 `output/current/` 正文；
- 清理或归档章节运行数据；
- 提出框架优化方案、diff 或变更计划，但在 KQ 批准前不得修改受保护文件。

## 变更授权流程

当确实需要修改框架时，必须先向 KQ 说明：

1. 准备修改哪些具体文件；
2. 为什么必须修改，新增旁路为什么不够；
3. 预计行为变化；
4. 回滚方式；
5. 等待 KQ 明确回复同意后才能执行。

模糊的“继续”“优化一下”“你看着办”不视为框架修改授权；必须能明确对应到本次框架变更。

## 冲突优先级

本文件高于仓库内其他普通说明。任何自动升级、重构、覆盖、同步操作与本协议冲突时，必须停止修改并请求 KQ 授权。

## 核心原则

> Writer 仓库是稳定生产线，不是实验沙盒。
> 可以外挂新能力，但未经 KQ 同意，不准改动已经跑通的主链。
