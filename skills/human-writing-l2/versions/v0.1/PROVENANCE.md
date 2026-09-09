# PROVENANCE｜Human Writing L2 Standalone

## 1. 来源

本 Skill 从历史仓库：

`kekaojip/-kq-novel-skills`

中的旧 `human-writing` L2 路线重新抽取。

主要基线提交：

`d82b0befc30bbe4b787d0ff765033d2b906d7efe`

该提交中的主文件标题为：

`活人感写作 1.9.0-L2｜LOCKED`

注意：该提交中的 `skills/human-writing/VERSION` 仍写着 `1.6.7`，版本元数据当时未完全同步；本 Skill 以主 `SKILL.md` 的 `1.9.0-L2｜LOCKED` 为历史语义基线。

## 2. 重点继承文件

历史主文件：

- `skills/human-writing/SKILL.md`
  - blob: `796429d833bae576d5a36c29a45110b18b2311cb`
- `skills/human-writing/references/web-fiction.md`
  - blob: `d7d032dc29090b8af48e4d04ca2047faef9f0ed2`
- `skills/human-writing/references/writer-positive-engine.md`
  - blob: `f1d229ba983b247a44deb80e7edeac6c053eed04`
- `skills/human-writing/references/revision.md`
  - blob: `d57edd788dcba0819eb4c475dbc5a88a442b7bf4`
- `skills/human-writing/references/fiction.md`
  - blob: `8af3eb4d7d1a1d890dd0ea1139df940c7e11bbbf`
- `skills/human-writing/scripts/check_prose.py`
  - blob: `e5fc64434ab167498f74edc0e30969189dd59050`

## 3. 本次处理方式

本目录不是历史文件的逐字镜像，而是一个新的独立 Skill。

保留：

- L2 五条核心正文原则；
- 商业网文“不完整权限”；
- 反逐条翻译；
- 够用即停；
- 延迟认知 / 延迟回应 / 延迟解决；
- 四类过度解决刹车；
- 局部返修而非全章洗稿；
- 扫描器只报警，不拥有改文权限。

不直接继承：

- 旧工作流的 `writer_brief` 强依赖；
- 旧 Controller / Builder / handoff_clean 路由；
- 旧 Reader Expectation / 三层卡接口；
- 与当前 Writer Runtime 已有题材 prose card 重复的 genre calibration；
- 非小说的论坛、现实文章、通用写作路由。

## 4. 独立性

本 Skill 当前：

`production_wired: false`

没有修改任何受 `FRAMEWORK_LOCK.md` 保护的现有 Writer Runtime 文件。

它只作为新增旁路能力存在。未来若要让 `START_HERE.md` 或 `story-writer-runtime/SKILL.md` 自动调用本 Skill，必须由 KQ 另行明确批准。