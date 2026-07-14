.PHONY: check hooks

# Run the repo's deterministic self-verification (T1 checker).
check:
	python3 tools/loopcheck.py

# Install the pre-push hook (version-controlled, under .githooks/).
# Zero-cost local enforcement — no CI minutes. When the repo goes public,
# add a GitHub Actions workflow that runs the same `make check` (free for
# public repos) as the binding gate for outside contributors.
hooks:
	git config core.hooksPath .githooks
	@echo "pre-push hook installed (core.hooksPath -> .githooks)"
