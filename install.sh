#!/bin/sh
# Loop Architect — one-line installer.
#
#   curl -fsSL https://raw.githubusercontent.com/Frontier-Intelligence-Lab/loop-architect/main/install.sh | sh
#
# Installs the loop-architect skill into your agent's skills directory.
# Override the target with:  CLAUDE_SKILLS_DIR=/path/to/skills sh install.sh
set -eu

REPO="Frontier-Intelligence-Lab/loop-architect"
ASSET_URL="https://github.com/${REPO}/releases/latest/download/loop-architect-skill.zip"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

say() { printf '%s\n' "$*"; }
die() { printf 'error: %s\n' "$*" >&2; exit 1; }

command -v curl >/dev/null 2>&1 || die "curl is required"

say "Loop Architect — installing into: $DEST"
mkdir -p "$DEST"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

say "Downloading latest release..."
curl -fsSL "$ASSET_URL" -o "$tmp/skill.zip" || die "download failed from $ASSET_URL"

say "Unpacking..."
if command -v unzip >/dev/null 2>&1; then
  unzip -oq "$tmp/skill.zip" -d "$DEST"
elif command -v bsdtar >/dev/null 2>&1; then
  bsdtar -xf "$tmp/skill.zip" -C "$DEST"
elif tar -xf "$tmp/skill.zip" -C "$DEST" 2>/dev/null; then
  : # macOS/libarchive tar can read zip
else
  die "need 'unzip' or a zip-capable 'tar' to unpack"
fi

[ -f "$DEST/loop-architect/SKILL.md" ] || die "install looked wrong — SKILL.md not found under $DEST/loop-architect"

say ""
say "✓ Installed: $DEST/loop-architect"
say "  Restart your agent (Claude Code / Codex) so it picks up the new skill."
say "  Then try:  \"Design a loop that keeps our dependencies up to date.\""
