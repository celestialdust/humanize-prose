---
name: humanize-prose
description: Revise academic, analytical, or essay prose so it reads as human-authored rather than AI-generated. Use this skill whenever a draft scores high on GPTZero, Turnitin AI, Originality.ai, Copyleaks, or any other AI-detection tool; whenever the user says "this reads too AI," "humanize this," "lower the AI score," "make this sound less AI," "rewrite in a human voice," or uploads an AI-detection report and asks for revision; and whenever the user wants to understand why clean academic prose trips AI detectors. Trigger this skill even if the user does not explicitly name it — if there is any AI-detection context or a writing task where human voice is the goal, prefer this skill over generic rewriting. Also applicable when composing original prose the user wants to read as human from the start.
---

# Humanize prose for AI detectors

## Why this skill exists

Academic, analytical, and essay prose is frequently flagged as AI-generated even when it is genuinely human-authored. The reason is not content. It is register. AI detectors score text on perplexity (how predictable each next word is) and burstiness (how much sentence-to-sentence variation exists). Smooth, tidy, evenly-paced expository writing — the kind a good student or an LLM both produce — scores high on AI probability because its register matches LLM output. Writing that reads human is not wilder or less polished; it is unevenly distributed. Specific where LLM writing is abstract. Clipped next to expansive. Carrying verifiable facts the model had to look up.

The principles in this skill are also plain good-prose principles: evidence density, structural asymmetry, resistance to over-refinement. Humanizing and writing well converge.

## The core insight (first-principles)

**The enemy is lexical-syntactic smoothness, not length or topic.**

An essay arguing a subtle thesis in 1,500 words can score 21% AI. The same essay lightly refined for tighter phrasing can score 66% AI. The content did not change. The register did.

Three corollaries follow.

1. **Evidence density is human.** Proper nouns, dated events, direct quotations with page citations, named scholars, verifiable historical facts — these are the strongest human-register signals a detector reads. Abstract analytical prose without them reads AI even when the argument is original.
2. **Cutting beats rewriting.** Removing words reduces the surface area where AI register can show. Rewriting the same content in tighter phrasing tends to *increase* AI register by smoothing the prose further.
3. **Asymmetry beats polish.** A long sentence next to a short one; a hedge next to a flat assertion; an unevenly-distributed paragraph length — these produce the burstiness detectors interpret as human.

## Workflow when the skill is triggered

Apply the steps in order. Do not skip Step 1.

### Step 1 — Diagnose before you edit

Read the draft end to end. Mark each paragraph as one of:

- **Evidence-dense** (has direct quotes, proper nouns, specific dates, or named historical detail throughout). These typically already read human. **Leave them alone.**
- **Analytical** (thesis, conclusion, framing, transitions). These are the AI-prone zones. Revision concentrates here.
- **Mixed** (one or two specifics embedded in otherwise abstract prose). Consider targeted cuts, not rewrites.

Also check structural balance. If one paragraph is more than twice the length of the shortest, the draft is probably unbalanced in a way detectors penalize.

### Step 2 — Cut, do not rephrase

Cutting is the single strongest move. Our reference trajectory (see `references/trajectory.md`) shows a 47-point AI-score drop from one round of cuts-plus-evidence, followed by two rounds of "surgical refinements" that regressed the score 45 points.

Delete on sight:

- Transitional paragraphs that summarize the previous paragraph before moving on
- Sentences that restate the thesis without adding evidence
- Any sentence that could begin with "Furthermore," "Moreover," "Thus," "Indeed," or "It is important to note"
- Metacommentary: "In this paper I will argue," "As will be shown," "The following section demonstrates"
- Two-adjective pairs that mean the same thing ("careful and thoughtful," "clear and direct")
- Clauses that exist to maintain parallel structure with another clause rather than to say something

If cutting leaves a paragraph stubby, that is fine. Short paragraphs contribute burstiness.

### Step 3 — Add evidence, not refinement

If a paragraph still reads AI after cutting, add **one** concrete specific. Good adds:

- A direct quotation from a cited source with page number: `(Author Year, 114)`
- A specific date (year plus month or season when available)
- A named scholar, film title with release year, historical figure, place name, or artifact
- A verifiable historical fact the paragraph's argument now rests on

One caution. Adding a specific to a paragraph that is already evidence-dense can *raise* the AI score because the insertion reads as retrieval-style scaffolding. Evidence works best in paragraphs that were abstract. If a paragraph is already dense, leave it.

### Step 4 — Remove AI-tell patterns

Scan and purge:

| Pattern | Fix |
|---|---|
| Em-dashes (—) | Replace with periods or parentheses. |
| Semicolons (;) | Split into two sentences. |
| Cleft constructions ("It is X that Y") | "X does Y." |
| Neat tricolons ("tightens, sharpens, and parallelizes") | Cut to two terms, or vary the pattern. |
| Causal sentence-fusion ("A, because B" where "A. B." also works) | Keep them apart. Short-next-to-short is more human. |
| Crisp metaphor verbs ("runs the aesthetic in reverse," "uses X as a vehicle for Y") | Flatter verbs. |
| Exhaustive adjective stacks ("soft, flat, childlike, pastel") | Pick two. |
| "illustrates," "underscores," "demonstrates," "highlights" | Use a plainer verb when the paragraph already states the point. |
| Topic-summary opener of a paragraph | Consider cutting. Let the evidence open the paragraph. |

A quick programmatic scan for some of these lives in `scripts/ai_tell_scan.py`.

### Step 5 — Introduce burstiness

Human writers produce uneven sentence lengths. Introduce contrast:

- After a long sentence, write a six-word one.
- Let a one-idea sentence stand alone where the prose has been smooth.
- Add a hedge ("in a sense," "something like," "almost," "not quite") next to a flat assertion.
- Drop a clipped clause mid-paragraph.

### Step 6 — Verify, then stop

Before running the detector again:

- Diff the new draft against the last-known-good version. If the new differences are mostly rephrasing rather than cuts or added evidence, expect regression.
- If the last score was already below 30%, you are likely at or near the local optimum for this draft. Further rewrites are more likely to hurt than help.
- If three successive rewrites score within 15 points of each other, **stop**. Submit the best version. Detector variance across runs is ±10–20 points, so smaller deltas are noise.

## What NOT to do

### The refinement trap

"Surgical improvements" that feel editorial — tightening phrasing, sharpening word choice, combining related short sentences for smoothness, making parallel structures cleaner — are the exact operations that push prose toward AI register. Copy-editor intuition is often anti-human-register.

### The more-effort trap

Scores do not move monotonically with effort. Our reference trajectory ran 75% → 68% → **21%** → 56% → 66% across successive careful rewrites. The last two rounds were thoughtful. They made things worse. If the draft is good enough, shipping beats rewriting.

### The rewrite-what's-working trap

Once a paragraph reads human, do not edit it — not even to tighten. In the reference trajectory, a draft preserved two middle paragraphs untouched (the ones reading green) and rewrote four others. All four regressed. The untouched two stayed green. **Preserve what works.**

### The chase-the-noise trap

A single 10-point movement across one detector run is not signal. Only act on consistent differences across two or more runs, or differences greater than 20 points.

## Red-flag scan (ship-readiness checklist)

Before submitting a draft to a detector:

- [ ] Zero em-dashes
- [ ] Zero semicolons
- [ ] Zero instances of "furthermore," "moreover," "thus," "indeed," "it is important to note"
- [ ] No tricolons with identical grammatical endings
- [ ] No two consecutive sentences joined by "because" where "A. B." reads naturally
- [ ] Paragraph word counts within a factor of 2–3 of each other, not one paragraph >2× the smallest
- [ ] Each paragraph contains at least one proper noun, date, or direct quote
- [ ] No two adjacent sentences have the same length (±3 words)
- [ ] Opening sentence of each body paragraph is not a topic-summary restatement
- [ ] Bibliography citations match in-text citations exactly

The script `scripts/ai_tell_scan.py` automates the first seven checks.

## What this skill does not claim

- It does not teach a user to pass off AI-generated writing as human. The principles work only when the content and argument are the user's own — evidence density requires the writer to actually know the sources, and asymmetric prose requires genuine thinking. An AI-generated draft of an unresearched topic will still read AI because it lacks retrievable specifics.
- It does not guarantee a specific score on any detector. Detectors are probabilistic and vary across runs.
- It does not apply well to fiction (already human-register by default), to short text under 300 words (where detectors are unreliable), or to heavy-jargon technical writing (where domain register dominates over prose register).

## Empirical basis

This skill was distilled from an eight-draft iteration of an academic essay (v1 → v8) graded repeatedly against GPTZero. The trajectory — what each edit changed and what the score did in response — is documented in `references/trajectory.md`. Read that file if you want to see the evidence before trusting the rules. Every principle above has at least one specific draft-to-draft comparison behind it.
