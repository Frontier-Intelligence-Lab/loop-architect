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
