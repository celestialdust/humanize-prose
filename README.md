# humanize-prose

A Claude skill for revising academic and analytical prose so it reads as human-authored rather than AI-generated. Built from empirical lessons across eight drafts of a real essay, where the GPTZero AI score moved 75% → 21% → 66% depending on what each rewrite did.

The principles also work as plain good-prose principles. Evidence density, structural asymmetry, resistance to over-refinement. Humanizing and writing well converge.

## Install

### Claude.ai

1. Download [`SKILL.md`](./SKILL.md) from this repo
2. In Claude.ai, open **Settings → Skills** and upload the file
3. Claude will automatically apply it when you ask to humanize prose or lower an AI-detection score

### Claude Code

```bash
curl -L -o ~/.claude/skills/humanize-prose.md \
  https://raw.githubusercontent.com/celestialdust/humanize-prose/main/SKILL.md
```

Restart Claude Code. The skill loads automatically.

### Claude API

Upload via the [Skills API](https://docs.claude.com/en/api/skills-guide):

```python
import anthropic

client = anthropic.Anthropic()
with open("SKILL.md", "rb") as f:
    skill = client.beta.files.upload(("SKILL.md", f, "text/plain"))
# pass skill.id in your Messages request
```

## What it does

Academic prose gets flagged as AI-generated even when it is genuinely human-authored. The reason is register. AI detectors score text on perplexity (how predictable each next word is) and burstiness (how much sentence-to-sentence variation exists). Smooth, tidy, evenly-paced expository writing scores high on AI probability because its register matches LLM output.

The skill walks Claude through a six-step revision workflow:

1. **Diagnose before editing.** Mark each paragraph as evidence-dense, analytical, or mixed. Leave the evidence-dense ones alone.
2. **Cut, do not rephrase.** Removing words is the single strongest move.
3. **Add evidence, not refinement.** A direct quote with page citation, a named scholar, a specific date.
4. **Remove AI-tell patterns.** Em-dashes, semicolons, "furthermore"/"moreover"/"thus," cleft constructions, causal sentence-fusion, crisp metaphor verbs.
5. **Asymmetrize.** Follow long sentences with short ones, add hedges next to flat assertions.
6. **Verify, then stop.** Detector variance is ±10–20 points. If three rewrites land within 15 points of each other, ship the best.

## Empirical basis

Every principle in `SKILL.md` has at least one draft-to-draft comparison behind it. The full trajectory is in [`references/trajectory.md`](./references/trajectory.md):

| Draft | Body words | GPTZero AI % | What changed |
|---|---|---|---|
| v3 | ~1,700 | 69% | Initial academic draft |
| v4 | 1,862 | 75% | Tighter phrasing, smoother transitions |
| v5 | 1,978 | 68% | Added "student-voice" texture |
| **v6** | **1,452** | **21%** | **Cut ~500 words; added direct quote + three dates** |
| v7 | 1,442 | 56% | Surgical refinements to yellow paragraphs |
| v8 | 1,456 | 66% | v6 + one evidentiary addition |

The one successful move (v5 → v6) dropped the score 47 points by cutting abstract filler and adding specifics. The two refinement moves that followed regressed the score 35 and 45 points despite feeling like improvements. Know when to stop.

## Contents

```
humanize-prose/
├── SKILL.md                      # The skill — workflow + red-flag scan
├── references/
│   └── trajectory.md             # Eight-draft empirical record
└── scripts/
    └── ai_tell_scan.py           # Programmatic red-flag check
```

## Using the scanner standalone

The scan script works on any markdown or plain-text draft:

```bash
python3 scripts/ai_tell_scan.py your_draft.md
```

It reports em-dash/semicolon counts, AI-tell phrase hits, weak analytic verbs, causal sentence-fusion ("X, because Y"), neat tricolons, paragraph balance, and sentence-length distribution.

## Scope

- Does not teach users to pass off AI-generated writing as human. The principles only work when the content and argument are the writer's own — evidence density requires actually knowing the sources.
- Does not guarantee a specific detector score. Detectors are probabilistic and vary across runs.
- Does not apply well to fiction, text under 300 words, or heavy-jargon technical writing.

## License

MIT. See [`LICENSE`](./LICENSE).

## Provenance

Built through an iterative collaboration between Joey Xue and Claude, distilled from a JPNS 162 essay trajectory in April 2026.
