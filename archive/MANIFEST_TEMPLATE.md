# Writer Archive Manifest Template

> 归档证据模板。归档不是小说真相源；最终真相仍在主仓正文与 Tracking。

```md
# Chapter {NNN} Archive Manifest

- project: {书名}
- chapter: {N}
- title: {章名}
- run_type: create | revision
- main_source_revision: {主仓 state_revision / commit，可得时填写}
- writer_workspace_commit: {Writer 输入发布 commit}
- writer_attempts: {1|2|3}

## Drafts
- draft.md: {present / sha / note}
- draft_v2.md: {present / sha / note}
- draft_v3.md: {present / sha / note}

## Review
- story_review: {PASS / CONCERNS / REJECT / summary}
- deslop_detect_only: {not_run / run + summary}
- final_main_verdict: PASS

## Accepted
- accepted_version: draft.md | draft_v2.md | draft_v3.md
- main_prose_path: {主仓 正文/第N章_*.md}
- tracking_state_revision_after_accept: {revision}
- tracking_commit: {commit / transaction id if available}

## Proposed Additions
- accepted: ...
- temporary: ...
- rejected: ...

## Notes
- {必要审计说明}
```

归档完成并确认 Tracking 同步后，Main 才把 `HANDOFF_STATE.status` 切为 `archived`，然后清理热区。
