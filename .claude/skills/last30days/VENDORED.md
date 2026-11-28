# last30days (vendored)

Vendored from https://github.com/mvanhorn/last30days-skill at commit 3fd9465 (v4.8.0, MIT).
Only the runtime skill tree is included: SKILL.md, references/, scripts/ (dev and eval scripts, agents/ and media assets left out per upstream .skillignore).
The upstream Claude Code plugin also registers a Stop hook (capture_brief_hook.py); a project skill install does not, so briefs are not auto-captured.
Upstream recommends the marketplace install for auto-updates: /plugin marketplace add mvanhorn/last30days-skill
