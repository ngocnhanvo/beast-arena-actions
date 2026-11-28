# 2026-11-28 — Walk height +2px approved trial

Owner explicitly approved the compared +2px Walk sprites for actual game. Private main source `3143db3e78a531806bcdeab254eb214f9192795d`; previous public docs baseline `a159b59aba075bbb700ba964c12c949025fae692`, latest prior production build #46130966383, Chromium #46131126049. Source height sequence is 76/74/76/75 instead of 74/72/74/73; widths, contact, Idle12, timing and game systems unchanged. No rejected redraw or new runtime auto-fit. Exact owner-preview pixel match checked in PRIVATE source regression. Existing build.yml and web-e2e.yml unchanged. This public docs-only push deliberately triggers build for new source. Wait build/Pages and downstream Chromium on this pipeline SHA and exact private source, inspect jobs/logs and record evidence. Anatomy/actual perceived-size review still pending.

**Trạng thái: PARTIAL — chưa hoàn tất.**
