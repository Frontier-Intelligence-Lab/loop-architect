# Contributing

Three things are especially welcome:

**1. Verifier patterns we're missing.** The ladder in `references/verifier-patterns.md` is the core of this skill. If you know an oracle we haven't listed — for a phase, a language, or a domain where verification is currently weak — that is the highest-value contribution possible.

**2. Loop types.** New patterns for `references/loop-types.md`, with the verifier and the safe autonomy level for each. Include what it's blind to.

**3. Failure stories.** Loops that burned you. Every anti-pattern in this skill was learned the expensive way; the honest post-mortems are worth more than the success stories.

## Ground rules

- **Keep principles tool-agnostic.** Anything specific to a product, model, or version belongs in `references/product-loop-notes.md` — with a citation and verification date, so it can be checked when it goes stale.
- **Cite claims.** No invented statistics. If it's unverified, say so. Use `references/evidence.md` for claim labels and citation hygiene.
- **Be pessimistic about verifiers.** When in doubt, assign the lower tier.

## Structure

Principles change slowly; product details change fast. Please respect that boundary — it's the reason this skill won't rot.

## Publishing the npm package

The public installer is **`@frontier-intelligence/loop-architect`** on the npm registry
(source: this repo, [Frontier-Intelligence-Lab/loop-architect](https://github.com/Frontier-Intelligence-Lab/loop-architect)).

It is **not** a library — `bin/loop-architect.js` copies `skills/loop-architect/` into
Claude/Codex skill dirs. Runner, evals, examples, and `tools/` stay git-only.

### One-time setup

1. Own or join the npm scope **`@frontier-intelligence`** (create the org if needed).
2. Authenticate: `npm login` (or a publish-capable `NPM_TOKEN` in CI).
3. Confirm: `npm whoami`.

### Every release

```bash
# bump version in package.json when needed (semver; same version cannot be republished)
npm pack --dry-run          # must include bin/ + skills/loop-architect/
npm publish --access public
npm view @frontier-intelligence/loop-architect version
```

Prefer publishing from a clean **`main`** commit you intend users to install.

Full checklist, CLI docs, troubleshooting, and how this relates to `npx skills` /
plugin / `curl` install paths: **[docs/npm-package.md](docs/npm-package.md)**.
