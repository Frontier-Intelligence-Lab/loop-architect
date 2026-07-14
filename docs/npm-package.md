# npm package: `@frontier-intelligence/loop-architect`

Public installer package for the Loop Architect skill. Source repo:
[Frontier-Intelligence-Lab/loop-architect](https://github.com/Frontier-Intelligence-Lab/loop-architect).

| Field | Value |
|---|---|
| **Package name** | `@frontier-intelligence/loop-architect` |
| **Registry** | [npmjs.com](https://www.npmjs.com/package/@frontier-intelligence/loop-architect) |
| **Current version** | `0.1.0` (see root `package.json`) |
| **License** | MIT |
| **Engines** | Node.js `>=16.7` (uses `fs.cpSync` / `fs.rmSync`) |
| **Binary** | `loop-architect` → `bin/loop-architect.js` |
| **Access** | Public (`publishConfig.access: "public"`) |

> **Naming note.** The GitHub org is `Frontier-Intelligence-Lab`. The npm **scope** is
> `@frontier-intelligence` (lowercase, hyphenated — npm scopes are case-insensitive and
> conventionally lowercased). Install with the scoped name, not the GitHub path.

---

## What this package is (and is not)

**Is:** a one-command installer that copies the skill tree from
`skills/loop-architect/` into Claude and/or Codex skill directories.

**Is not:** a runtime library, API client, or agent runner. After install, the agent
reads plain markdown (`SKILL.md` + references + templates). No Node dependency is
required at *use* time — only for the installer.

Other install paths (`npx skills add`, Claude plugin marketplace, `curl | sh`, manual
copy) install the **same** skill content. Prefer whichever fits your harness.

---

## Install (end users)

Requires Node 16.7+ and network access to the npm registry.

```bash
# Recommended — install into both Claude and Codex if present
npx @frontier-intelligence/loop-architect install --target both

# Claude only
npx @frontier-intelligence/loop-architect install --target claude

# Codex only
npx @frontier-intelligence/loop-architect install --target codex

# Overwrite an existing install
npx @frontier-intelligence/loop-architect install --target both --force

# Auto-detect (~/.claude and/or ~/.codex markers; defaults to Claude if neither exists)
npx @frontier-intelligence/loop-architect install
```

### Install locations

| Target | Default directory | Override |
|---|---|---|
| Claude | `~/.claude/skills/loop-architect` | `CLAUDE_SKILLS_DIR` (parent skills dir) |
| Codex | `~/.codex/skills/loop-architect` | `CODEX_SKILLS_DIR` (parent skills dir) |

### After install

1. **Restart** the agent so it reloads skills.
2. Smoke-test with a design or audit prompt (see root [README.md](../README.md#smoke-test)).

### CLI reference

```text
loop-architect <version> — installer for the Loop Architect skill

Usage:
  npx @frontier-intelligence/loop-architect install [options]

Options:
  -t, --target <codex|claude|both>   where to install (default: auto-detect)
  -f, --force                        overwrite an existing install
  -h, --help                         show help
  -v, --version                      print package version
```

The only command is `install`. Omitting the command also runs `install`.

### What ships in the tarball

Controlled by `package.json` `files` (plus always-included `package.json`, `README.md`, `LICENSE`):

```
bin/loop-architect.js
skills/loop-architect/          # full skill payload (SKILL.md, agents/, references/, assets/)
```

Runner, evals, examples, adapters, and `tools/loopcheck.py` live in the **git repo** only;
they are not part of the npm package.

Verify locally before publish:

```bash
npm pack --dry-run
```

---

## Publish (maintainers)

### Prerequisites

1. **npm account** with permission to publish under the `@frontier-intelligence` scope.
2. **Scope ownership.** The org/scope `@frontier-intelligence` must exist and your
   account must be a member with publish rights. First-time setup:
   - Create the org at [npmjs.com/org/create](https://www.npmjs.com/org/create) named
     `frontier-intelligence` (or claim the scope via your org settings), **or**
   - Publish under a personal account that owns that scope.
3. **Auth on the machine** (pick one):

```bash
# Interactive (browser / OTP)
npm login
npm whoami   # must print your npm username

# CI / headless — granular access token with publish permission
# https://www.npmjs.com/settings/~/tokens
npm config set //registry.npmjs.org/:_authToken "$NPM_TOKEN"
```

4. **Clean package tree** — publish from a commit you intend to release (prefer `main`
   after merge). Root `package.json` `version` is the source of truth.

### Release checklist

```bash
# 1. Confirm identity and that this version is not already on the registry
npm whoami
npm view @frontier-intelligence/loop-architect version   # 404 is OK for first publish

# 2. Sanity-check package contents
npm pack --dry-run
# Expect: bin/ + skills/loop-architect/** + LICENSE + README + package.json

# 3. Optional local install smoke test from packed tarball
npm pack
npx --yes ./frontier-intelligence-loop-architect-0.1.0.tgz install --help

# 4. Publish (scoped packages need public access for open install)
npm publish --access public

# 5. Verify
npm view @frontier-intelligence/loop-architect name version
npx --yes @frontier-intelligence/loop-architect@0.1.0 --version
```

### Version bumps

Follow semver for the **installer + bundled skill** as a unit:

| Change | Bump |
|---|---|
| Skill wording / templates / references only | patch (`0.1.0` → `0.1.1`) |
| Installer CLI flags, paths, or install targets | minor if compatible; major if breaking |
| Breaking CLI or removal of skill paths users rely on | major |

```bash
# edit package.json "version", or:
npm version patch   # also creates a git tag if you use npm's versioning workflow
npm publish --access public
git push && git push --tags
```

**You cannot republish the same version.** If `0.1.0` is wrong, publish `0.1.1`.

### What not to do

- Do not force-publish or unpublish casually — npm unpublish rules are strict after 72h.
- Do not publish secrets; the tarball is public. Only `bin/` and `skills/loop-architect/` ship.
- Do not change the package **name** without a migration plan; `npx` users pin the scoped name.
- Do not publish from a dirty worktree with unrelated local experiments.

### Linking GitHub ↔ npm (optional)

On the npm package page, set the repository URL to
`https://github.com/Frontier-Intelligence-Lab/loop-architect` (already in `package.json`
`repository` / `homepage` / `bugs`). That matches the GitHub org path users expect even
though the npm scope spelling differs.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `ENEEDAUTH` / need auth | Not logged in | `npm login` or set `//registry.npmjs.org/:_authToken` |
| `404` on `npm view` before first publish | Package not published yet | Expected; run `npm publish --access public` |
| `403` / not authorized for scope | Scope org missing or no publish role | Create/join `@frontier-intelligence` org; get publish rights |
| `EPUBLISHCONFLICT` / version exists | Version already published | Bump `package.json` version |
| Install says skill already exists | Previous install present | Re-run with `--force` |
| Agent doesn't see the skill | Stale session | Restart agent after install |
| `skill payload missing` | Broken package / wrong `files` | Ensure `skills/loop-architect/SKILL.md` is in the tarball |

---

## Related install methods

| Method | Command / path |
|---|---|
| **npm (this doc)** | `npx @frontier-intelligence/loop-architect install` |
| npx skills | `npx skills add Frontier-Intelligence-Lab/loop-architect` |
| Claude plugin marketplace | `/plugin marketplace add Frontier-Intelligence-Lab/loop-architect` |
| curl installer | `curl -fsSL …/install.sh \| sh` |
| Manual | copy `skills/loop-architect` → `~/.claude/skills/` or `~/.codex/skills/` |

All of these install the skill under `skills/loop-architect/` from this repository.
The npm package is the **branded Node installer** path; see the root [README.md](../README.md#install).
