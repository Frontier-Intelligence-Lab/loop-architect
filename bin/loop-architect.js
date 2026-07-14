#!/usr/bin/env node
'use strict';

// Loop Architect installer.
//   npx @frontier-intelligence/loop-architect install [--target codex|claude|both] [--force]
//
// Copies the bundled skill into your agent's skills directory. The skill payload
// ships inside this package, so paths resolve relative to THIS file (__dirname),
// not the caller's working directory.

const fs = require('fs');
const os = require('os');
const path = require('path');

const PKG = require('../package.json');
const SKILL_NAME = 'loop-architect';
const SRC = path.join(__dirname, '..', 'skills', SKILL_NAME);

const TARGETS = {
  claude: {
    label: 'Claude',
    home: process.env.CLAUDE_SKILLS_DIR || path.join(os.homedir(), '.claude', 'skills'),
    // parent that signals "this agent is set up on this machine"
    marker: path.join(os.homedir(), '.claude'),
  },
  codex: {
    label: 'Codex',
    home: process.env.CODEX_SKILLS_DIR || path.join(os.homedir(), '.codex', 'skills'),
    marker: path.join(os.homedir(), '.codex'),
  },
};

function log(msg) { process.stdout.write(String(msg) + '\n'); }
function die(msg) { process.stderr.write('error: ' + msg + '\n'); process.exit(1); }

function parseArgs(argv) {
  const args = { _: [], target: null, force: false, help: false, version: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--force' || a === '-f') args.force = true;
    else if (a === '--target' || a === '-t') args.target = argv[++i];
    else if (a.startsWith('--target=')) args.target = a.slice('--target='.length);
    else if (a === '--help' || a === '-h') args.help = true;
    else if (a === '--version' || a === '-v') args.version = true;
    else args._.push(a);
  }
  return args;
}

function help() {
  log(`loop-architect ${PKG.version} — installer for the Loop Architect skill

Usage:
  npx @frontier-intelligence/loop-architect install [options]

Options:
  -t, --target <codex|claude|both>   where to install (default: auto-detect)
  -f, --force                        overwrite an existing install
  -h, --help                         show this help
  -v, --version                      print version

Examples:
  npx @frontier-intelligence/loop-architect install --target claude
  npx @frontier-intelligence/loop-architect install --target codex
  npx @frontier-intelligence/loop-architect install --target both --force`);
}

function chosenTargets(target) {
  if (target === 'both') return ['claude', 'codex'];
  if (target === 'claude' || target === 'codex') return [target];
  if (target) die(`unknown --target "${target}" (use: codex, claude, or both)`);
  // auto-detect: install where an agent home already exists; default to claude
  const detected = ['claude', 'codex'].filter((k) => fs.existsSync(TARGETS[k].marker));
  if (detected.length) return detected;
  log('No ~/.claude or ~/.codex found — defaulting to Claude. Use --target to override.');
  return ['claude'];
}

function installTo(key, force) {
  const t = TARGETS[key];
  const dest = path.join(t.home, SKILL_NAME);
  if (fs.existsSync(dest) && !force) {
    die(`${t.label}: ${dest} already exists.\n       Re-run with --force to overwrite it.`);
  }
  if (fs.existsSync(dest)) fs.rmSync(dest, { recursive: true, force: true });
  fs.mkdirSync(t.home, { recursive: true });
  fs.cpSync(SRC, dest, { recursive: true });
  if (!fs.existsSync(path.join(dest, 'SKILL.md'))) {
    die(`${t.label}: install verification failed — SKILL.md not found in ${dest}`);
  }
  log(`  ✓ ${t.label}: ${dest}`);
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.version) { log(PKG.version); return; }
  if (args.help) { help(); return; }

  const cmd = args._[0] || 'install';
  if (cmd !== 'install') die(`unknown command "${cmd}" — the only command is: install (see --help)`);

  if (!fs.existsSync(path.join(SRC, 'SKILL.md'))) {
    die(`skill payload missing at ${SRC} — the package looks built incorrectly`);
  }

  const targets = chosenTargets(args.target); // validates --target before any output
  log('Loop Architect — installing the skill:');
  for (const key of targets) installTo(key, args.force);

  log('');
  log('Done. Restart your agent so it picks up the skill, then try:');
  log('  "Design a loop that keeps our dependencies up to date."');
  log('  "Is this cron job safe to run unattended?"        (audit mode)');
  log('  "Auto-fix production incidents with an agent."     (expect a reasoned no)');
}

main();
