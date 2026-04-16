# Workflow

## 1. Audit First

Before writing copy or enriching anything, inspect the CSV and quantify:
- row count
- email coverage
- LinkedIn coverage
- top job titles
- top industries
- duplicate company concentration
- missing intent fields

If the actual data contradicts the file name or user framing, call that out early.

## 2. Ask Focused Questions

Questions should only resolve decisions that affect:
- filtering
- offer framing
- proof selection
- Blitz credit usage
- CTA priority

## 3. Read Proof Sources

Read the proof document before writing copy. Extract:
- named customer results
- meeting-booked outcomes
- speed-to-pipeline outcomes
- cost/ramp replacement angles
- risk-reversal angles

Prefer proof that matches the audience and offer.

## 4. Clean and Enrich

Clean these fields before copy:
- contact names
- company names
- job titles
- company display names

Preserve verified emails already in the list.
Only enrich blanks unless the user explicitly asks to validate or overwrite existing emails.

Use LinkedIn URL first for Blitz `/enrichment/email`.

## 5. QC Emails

Always compare the primary email domain against the company domain.

Use:
- `safe_match` when domains align
- `mismatch_review` when they do not
- `missing` when no primary email exists

Do not claim the full list is safe just because a tool returned an email.

## 6. Build Personalization Columns

Do not jump straight to copy.

Generate campaign-ready columns first:
- company display field
- role bucket
- angle bucket
- pain hook
- growth hook
- proof line
- tailored message or short intro

Keep the columns short enough to use in sequencers.

## 7. Write Copy

Write copy against the real columns, not imagined placeholders.

Default sequence:
- 2 variants for Email 1
- 2 variants for Email 2
- 1 variant for Email 3

Use spintax only after the base copy is stable.

Rules:
- no em dashes
- soft CTAs
- no links in first email unless explicitly requested
- pain-led and growth-aware

## 8. Package Outputs

Typical outputs:
- cleaned master CSV
- copy doc
- sequencer-ready spintax file
- copied assets in user-requested folder
