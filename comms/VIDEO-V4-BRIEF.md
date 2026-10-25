Package: **nightshift-v4-package.zip** in the team Drive folder — https://drive.google.com/drive/folders/1s05dJalaNxuFaOfgRjMlKlo4MHqvow-s

# VIDEO V4 — RE-CUT BRIEF FOR RENE-CLAUDE
*From TREE, per Rene's direction · 2026-10-25, ~16:05 PT · Team: bino force go · Product: NightShift*

## The ask
Re-cut the NightShift film. Rene's verdict on v3: **"styling is a little off — feels like slides."** He's right, and here's the honest diagnosis: v3 is five static full-screen cards, hard cuts exactly on the narration lines, no motion inside any shot, typography doing all the work. It plays as a deck with a voiceover. Remake it as a **film** — A24 trailer grammar, not slide grammar — something that grabs attention in the first seconds and holds it.

## What you're getting (this package)
- `takes/take1.mp4` — hero screen: 23 → 8 → 7 → 0 count-up, approval queue, live machine panel (14.0s)
- `takes/take2.mp4` — Act I, the night: 23 items arriving as 8 cluster stories (11.6s)
- `takes/take3.mp4` — Act II, the gate: cursor glides to APPROVE, **real click**, receipt stamps live at 15:46:15 PT (15.7s)
- `takes/take4.mp4` — Act III, the machine: live prompt fired at qwen36 mid-take, **token counter climbs 7,358 → 8,491**, GPU temp rises (12.0s)
- `takes/take5.mp4` — Act IV, the receipts wall auto-scrolling + end card (13.5s)
  All takes: real screen recordings from the GB10 itself, 1920×1200, ~24fps.
- `audio/N1..N5.mp3` — Helio narration, one line per act (the brand voice; reuse and re-time freely — if you want new lines, flag it in the LOG and Tree will voice them)
- `nightshift-a24-v3.mp4` — the current cut, as the "before" reference
- `ui/` — the five screen sources (the live UI also runs on the box at `~/nightshift-ui/`, served on :8800, if you want fresh captures)
- `scripts/` — `record_journey.py` (how the takes were captured), `render3.py` + `gen_data.py` (how v3 was assembled / where the live telemetry comes from)

## The film to make
- **Hook in the first 3 seconds.** Open on motion — the token counter already climbing, or the cursor already travelling toward APPROVE. No opening title card. If a title appears, it arrives late, small, in a corner — or over black at the very end.
- **Every shot must live.** Slow push-ins and zooms into details of the real captures: the receipt stamping, the BLOCKED egress rows, the 0 in the count-up, the token numbers rolling. Cursor movement, the receipts scroll. A still frame is allowed only as a held breath — a beat, never a page.
- **Type as punctuation, not pages.** Small caps supers in corners and margins, one short line at a time. Never a full-screen headline with a paragraph under it. One exception: the end card, one line over black — *"An agent you can leave alone with the business — because it can't act alone."*
- **Rhythm uneven on purpose.** A fast cluster up front (the night arriving), then a long quiet hold on the gate before the click — the click should land like a gunshot, silence around it — then release into the receipts. Leave air around the narration; the voice should feel like it's commenting on a film, not reading a deck aloud.
- **Sound.** Re-time the Helio lines against picture. A sparse bed if you have one — single piano/synth motif, room tone — A24 trailers run on one motif and silence. No whooshes, no corporate stingers, no trailer braams.
- **Finish.** Subtle grain/vignette is fine, speed ramps on the cursor glides are fine, dip-to-black and crossfades between acts instead of hard cuts everywhere. Don't over-grade it into mush — the screen detail (numbers, draft text) must stay legible.
- **Length:** 45–75 seconds. Hard cap under 2:00 (submission rule).

## Hard facts — do not invent or alter
- 23 items in → 8 clusters → 7 drafts → **0 sent**. Tokens climb **7,358 → 8,491** during the live prompt. Receipt stamped **15:46:15 PT**.
- Model: **qwen36** (Qwen3.6-35B-A3B-heretic, NVFP4) served locally on a **Dell Pro Max with GB10**. Egress from the sandbox: github.com, api.nvidia.com, pypi.org, registry.npmjs.org, example.com all **BLOCKED**; only inference.local allowed.
- The Q2 draft text on the gate screen is the real model draft — if you zoom there, keep it legible; never paraphrase it on screen.
- Only real captures of the actual UI/box. No mockups, no stock, no fake UI, no invented numbers. The vLLM API key appears in nothing here — keep it that way.
- Names: product **NightShift**, team **bino force go**.

## Logistics
- **v3 stays in submission field 4** until your cut exists and Rene approves the swap. Do not touch the dashboard.
- **Deliver:** upload the finished MP4 to the same team Drive folder this package is in, and post a LOG entry (file name + duration + one line on what you changed). Tree uploads it to YouTube unlisted and swaps field 4 on Rene's OK.
- **Clock:** target the film in Drive by **16:50 PT**; hard latest **17:15 PT**. (Organizers' cutoff 18:00; Rene submits ~17:00 with v3 if v4 isn't ready — beat that.)
- **Box rules still hold** if you re-record: Rene's standing NO-RESTARTS rule — vLLM, Docker, and services stay untouched. The UI server (:8800) and `gen_data.py` are running on the box.
