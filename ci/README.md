# ci/ — staged CI (not active yet)

This folder holds a GitHub Actions workflow that is **intentionally not installed.** It
lives here, not in `.github/workflows/`, so it does **not** run — this repo is private
and GitHub Actions bills private-repo minutes.

## While the repo is private
Enforcement is local and free — no CI minutes:

```sh
make hooks     # once: installs the pre-push hook
make check     # runs the same checks CI would
```

## When you make the repo public
Actions is free for public repos with standard runners. Activate the gate:

```sh
mkdir -p .github/workflows
git mv ci/loopcheck.yml .github/workflows/loopcheck.yml
git commit -m "ci: enable loopcheck on PRs"
```

That's the whole migration — the workflow just runs `make check`, the same command the
pre-push hook already runs. Deterministic checks are the **required** gate. The behavioral
`evals/` stay manual/scheduled, never a blocking PR check (they're a weak, judged verifier
— gating on them would be the exact mistake this skill warns about).
