# Environment Strategy

Humanifest is the control repository. External repositories belong in separate workspaces, Codespaces, cloud environments, VMs, or dedicated workers. Do not vendor or submodule target repositories here.

## Decision Ladder

- Tier 0: evidence-only research, no clone and no dependency execution.
- Tier 1: read-only repository inspection, clone only when needed and do not install dependencies.
- Tier 2: bounded local worktree for trusted lightweight repositories.
- Tier 3: reproducible isolated environment using devcontainer, Docker, Codespaces, Codex Cloud, or disposable VM.
- Tier 4: dedicated worker for privileged Docker, invasive native setup, hardware-specific work, very high resource use, or recurring high-risk external OSS work.

## Current Recommendation

Do not configure a second computer yet. Use Codespaces or an existing devcontainer for unknown external OSS, Codex worktrees for Humanifest-local work, and local Docker only after inspecting privileges and lifecycle scripts.

Reconsider a second computer after repeated privileged Docker/native-installer work, persistent x86/ARM friction, or if cleanup and secret isolation become routine costs.
