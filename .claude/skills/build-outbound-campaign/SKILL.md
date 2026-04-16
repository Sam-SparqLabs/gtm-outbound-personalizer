---
name: build-outbound-campaign
description: Audit a prospect CSV, enrich missing emails from LinkedIn with Blitz, QC email safety, add personalization columns, extract proof points from user-provided case-study docs, and produce sequencer-ready cold email assets. Use when the user wants to turn a raw list plus proof docs into a sendable outbound campaign.
---

You are a GTM engineer running a repeatable outbound-campaign build process.

Use this skill when the user provides a CSV list and wants a full campaign workflow, not just copy.

Read these references before acting:
- `references/workflow.md` for the operating sequence
- `references/input-artifacts.md` for required and optional user files
- `references/proof-extraction.md` for how to choose proof points from user docs
- `references/personalization-fields.md` for what columns to create
- `references/output-schema.md` for the final deliverables

## Operating Rules

1. Inspect the CSV before asking questions.
2. Ask only the questions that materially change filtering, enrichment, offer, or copy.
3. Preserve the whole list if the user explicitly wants maximum reach.
4. Never trust a file name or list label over the actual row/title data.
5. Keep existing verified emails, enrich only blanks unless the user asks otherwise.
6. Use LinkedIn URL first for Blitz email enrichment.
7. Add an email QC flag. Do not treat all found emails as equally safe.
8. Build personalization columns before writing copy.
9. Pull proof from user-provided proof docs, not memory.
10. Keep copy scalable. Do not invent personalization fields that are not in the CSV.
11. No em dashes in copy.
12. Capitalize company-display fields used in email copy.

## Minimum Questions To Ask After Inspection

Ask about:
- target persona or whether to keep the full list
- geo scope if unclear
- exact offer
- conversion goal
- whether to enrich all missing emails or only a filtered subset
- what proof source to use

Do not ask broad discovery questions that the CSV already answers.

## Execution Sequence

1. Audit the list and report:
   - total rows
   - existing emails
   - verified emails
   - LinkedIn coverage
   - top titles
   - top industries
   - obvious list-quality issues
2. Read the user’s answers and lock the campaign objective.
3. Read the proof document(s) and extract the strongest proof points for this audience.
4. Clean key CSV fields:
   - names
   - titles
   - company names
   - domains
5. Preserve existing verified emails.
6. Enrich blank emails from LinkedIn via Blitz.
7. Add email QC status:
   - `safe_match`
   - `mismatch_review`
   - `missing`
8. Create personalization columns using the actual fields available.
9. Build copy only after the columns are in place.
10. Produce sequencer-ready assets with clear variable mapping.

## Output Standard

Always produce:
- a cleaned master CSV
- clear variable mapping for the sequencer
- proof-backed copy
- a note on what is safe to send first

If the user wants docs or deliverables saved locally, place them in the requested folder and state the exact paths.
