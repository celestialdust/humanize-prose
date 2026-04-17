# humanize-prose

A Claude skill for revising academic and analytical prose so it reads as human-authored rather than AI-generated. It applies empirical lessons from iterating an actual essay through eight drafts against GPTZero, where the score moved from 75% AI to 21% AI and back up to 66% depending on what each rewrite did.

The principles in the skill also work as plain good-prose principles. Evidence density, structural asymmetry, resistance to over-refinement. Humanizing and writing well converge.

## What the skill does

Academic prose gets flagged as AI-generated even when it is genuinely human-authored. The reason is register. AI detectors score text on perplexity (how predictable each next word is) and burstiness (how much sentence-to-sentence variation exists). Smooth, tidy, evenly-paced expository writing scores high on AI probability because its register matches LLM output. Writing that reads human is unevenly distributed. Specific where LLM writing is abstract. Clipped next to expansive. Carrying verifiable facts the model had to look up.

The skill walks Claude through a six-step revision workflow:

1. **Diagnose before editing.** Mark each paragraph as evidence-dense, analytical, or mixed. Leave the evidence-dense ones alone.
2. **Cut, do not rephrase.** Removing words is the single strongest move.
3. **Add evidence, not refinement.** A direct quote with page citation, a named scholar, a specific date.
4. **Remove AI-tell patterns.** Em-dashes, semicolons, "furthermore"/"moreover"/"thus," cleft constructions, causal sentence-fusion, crisp metaphor verbs.
5. **Asymmetrize.** Follow long sentences with short ones, add hedges next to flat assertions.
6. **Verify, then stop.** Detector variance is ±10–20 points. If three rewrites land within 15 points of each other, ship the best.

## Empirical basis

Every principle in `SKILL.md` has at least one draft-to-draft comparison behind it. The full trajectory lives in `references/trajectory.md`:

| Draft | Body words | GPTZero AI % | What changed |
|---|---|---|---|
| v3 | ~1,700 | 69% | Initial academic draft |
| v4 | 1,862 | 75% | Tighter phrasing, smoother transitions |
| v5 | 1,978 | 68% | Added "student-voice" texture |
| **v6** | **1,452** | **21%** | **Cut ~500 words; added direct quote + three dates** |
| v7 | 1,442 | 56% | Surgical refinements to yellow paragraphs |
| v8 | 1,456 | 66% | v6 + one evidentiary addition |

The one successful move (v5 → v6) dropped the score 47 points by cutting abstract filler and adding specifics. The two refinement moves after that (v6 → v7, v6 → v8) regressed the score 35 and 45 points respectively, despite feeling like improvements. The meta-lesson is in the trajectory itself: know when to stop.

## Installation

### As a Claude Code / Cowork skill

Drop the folder into your skills directory, or install the packaged bundle:

```bash
# Folder install — put this repo inside your skills dir
~/.claude/skills/humanize-prose/

# Or install the packaged .skill bundle
cp humanize-prose.skill ~/Downloads/
# Then open it from Claude Code or Cowork's skill installer
```

### As a reference

The skill is readable as plain markdown. Open `SKILL.md` and `references/trajectory.md` directly.

## Contents

```
humanize-prose/
├── SKILL.md                      # The skill itself — workflow + red-flag scan
├── references/
│   └── trajectory.md             # Eight-draft empirical record
├── scripts/
│   └── ai_tell_scan.py           # Programmatic red-flag check
└── humanize-prose.skill          # Packaged bundle for easy install
```

## Using the scanner standalone

The scan script works on any markdown or plain-text draft:

```bash
python3 scripts/ai_tell_scan.py your_draft.md
```

It reports em-dash/semicolon counts, AI-tell phrase hits, weak analytic verbs, causal sentence-fusion ("X, because Y"), neat tricolons, paragraph balance, and sentence-length distribution. It catches real regressions: on the reference trajectory, the script correctly detected the v6 → v7 regression as an increase in "because" fusion count (1 → 2) and a drop in short-sentence share (25% → 21%).

## What the skill does not claim

- It does not teach a user to pass off AI-generated writing as human. The principles work only when the content and argument are the user's own. Evidence density requires the writer to actually know the sources. Asymmetric prose requires genuine thinking. An AI-generated draft of an unresearched topic will still read AI because it lacks retrievable specifics.
- It does not guarantee a specific score on any detector. Detectors are probabilistic and vary across runs.
- It does not apply well to fiction, to short text under 300 words, or to heavy-jargon technical writing.

## License

MIT. See `LICENSE`.

## Provenance

Built through an iterative collaboration between Joey Xue and Claude, distilled from the JPNS 162 essay trajectory in April 2026.
