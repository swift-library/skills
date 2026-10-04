# Codex Exec Plans Basis

This note adapts OpenAI's Codex guidance for larger multi-step work:

- [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans)

For this skill, the active execution-state artifact is `.agent/PLANS.md`, built
from `templates/.agent.PLANS.md.tpl`. Use it when a normalize, migration, or
export task is too large for a one-shot pass, likely to span multiple sessions,
or needs explicit validation checkpoints.

Keep the plan self-contained, milestone-based, and current as discoveries land.
Do not let it become a substitute for architecture documentation, proposals,
decision records, GitHub governance, or `.codex` skill and capability
configuration.
