# Kick2 native QA watchdog (2026-11-28)

Previous private 0df2fbdcbf951d0fe71c13f8eb014ba55ccc7f21, public 6ca7bf2da19e189b2c46adcebb0b0c76e3d7306c, build #46161904467 was still IN_PROGRESS at native Character Visual Contract smoke (Godot command produced no terminal result in initial polling). Corrective Private 18368f820aa234ef229f19690dce76ed71e3f53d adds native SceneTree 18-second watchdog; public adds 45-second shell timeout on exactly this smoke step (not skips). The stale run cannot establish deploy success. New build must test actual smoke and Pages + Chromium with expected Private SHA. Strict visual authoring of legacy Idle/Walk remains pending. 

**Trạng thái: PARTIAL — chưa hoàn tất.**
