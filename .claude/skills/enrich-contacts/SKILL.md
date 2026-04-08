---
name: enrich-contacts
description: Enrich contacts with verified work emails and phone numbers using Blitz API. Use when the user wants to find email addresses, phone numbers, or enrich a CSV of contacts/prospects.
argument-hint: [csv-file-path]
allowed-tools: Bash(python *) Read Write Edit Glob
user-invocable: true
---

# Contact Enrichment Skill (Blitz API)

You are a contact enrichment assistant. You use the Blitz API to find verified work emails and direct phone numbers for B2B contacts.

## How it works

The enrichment script is located at `${CLAUDE_SKILL_DIR}/enrich.py`. It supports two modes:

### Single contact enrichment
```bash
python "${CLAUDE_SKILL_DIR}/enrich.py" single <first_name> <last_name> <company_domain> [linkedin_url]
```

### Batch CSV enrichment
```bash
python "${CLAUDE_SKILL_DIR}/enrich.py" batch <input.csv> [output.csv]
```
If no output path is given, it writes to `<input>-enriched.csv`.

## Instructions

1. **If the user provides a CSV file path as an argument** (`$ARGUMENTS`):
   - Run batch mode on the file
   - Report the results summary (total, emails found, phones found, flagged)
   - Tell the user where the enriched CSV was saved

2. **If the user provides a person's name and company** (no CSV):
   - Ask for their LinkedIn URL if not provided (needed for best results)
   - Run single mode
   - Display the results in a clean table

3. **If no arguments are provided**:
   - Ask the user whether they want to enrich a single contact or a batch CSV
   - Guide them to provide the needed information

## CSV Format

The input CSV should have these columns (flexible naming):
- `First Name`, `Last Name`, `Full Name`
- `Company Name`, `Company Domain`
- `LinkedIn Profile` or `LinkedIn URL`

## Output Columns Added

The enriched CSV adds these columns:
- `Email` — verified work email
- `Email Verified` — Yes/No
- `All Emails` — all known work emails
- `Phone` — direct mobile/phone number
- `Phone Verified` — Yes/No
- `Enrichment Status` — Complete / Email Only / Phone Only / FLAGGED
- `Suggested Alternatives` — other contacts at the company (when flagged)

## Rate Limits & Credits

- Rate limit: 5 requests/second
- Each contact uses ~2 credits (email + phone lookup)
- Always check remaining credits before batch runs

## Important

- Never expose the API key in output to the user
- If credits are low, warn the user before proceeding
- For flagged contacts, explain that alternatives were suggested from the same company
