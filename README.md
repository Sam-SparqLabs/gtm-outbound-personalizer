# GTM Outbound Personalizer

A Claude Code skill and Python toolkit that takes a CSV of companies/contacts and generates personalized outbound email columns.

## What It Does

Takes a raw prospect list and adds 3 columns:

| Column | What It Does |
|---|---|
| **Target ICP** | One-line summary of what the company does, flows naturally in email copy |
| **Outbound Gap** | TRUE / WARM / FALSE classification based on whether they offer outbound |
| **Target Column** | Personalized one-liner referencing their specific services and gap |

## Quick Start

### As a Claude Code Skill

Copy `.claude/skills/personalize-outbound/` to your project or `~/.claude/skills/` for global access.

Then run:

```
/personalize-outbound path/to/your/list.csv
```

### As a Standalone Script

```bash
python scripts/enrich_csv.py input.csv output.csv
```

## Email Sequence

See `.claude/skills/personalize-outbound/email-sequence-template.md` for a ready-to-use 5-email sequence (2 variants for Email 1 and 2, 1 breakup) that uses the generated columns.

## Additional Skill

This repo also includes `.claude/skills/build-outbound-campaign/` for the fuller campaign workflow:

- audit the raw CSV
- ask only the critical setup questions
- enrich missing emails from LinkedIn via Blitz
- QC email safety with domain-match flags
- extract proof points from user-provided proof docs
- add personalization columns
- produce sequencer-ready cold email assets

## CSV Requirements

Your CSV should have these columns (names are flexible):
- Company name
- Company description/bio
- Industry/sector
- First name
- Service description

## Outbound Gap Logic

- **TRUE** (typically 90%+) - no mention of outbound, SDR, cold email, or lead gen
- **WARM** (typically 3-7%) - mentions lead gen or demand gen but not outbound execution
- **FALSE** (typically <2%) - explicitly mentions outbound, SDR, or cold email
