# Enrich Contacts — Claude Code Skill

A Claude Code skill that enriches B2B contacts with verified work emails and direct phone numbers using the [Blitz API](https://blitz-api.ai/).

## Setup

### 1. Get a Blitz API Key

Sign up at [app.blitz-api.ai](https://app.blitz-api.ai) to get your API key (starts with `blitz-`). New accounts get 100 free credits.

### 2. Configure Your API Key

Open `enrich.py` and replace the API key on line 7:

```python
API_KEY = "blitz-your-api-key-here"
```

### 3. Install the Skill

Copy the `enrich-contacts/` folder to your Claude Code skills directory:

```bash
# Personal (available across all projects)
cp -r enrich-contacts/ ~/.claude/skills/enrich-contacts/

# Or project-level (this project only)
cp -r enrich-contacts/ .claude/skills/enrich-contacts/
```

No external dependencies required — uses only Python standard library.

## Usage

### In Claude Code

**Enrich a CSV file:**
```
/enrich-contacts C:\Users\you\Downloads\prospects.csv
```

**Enrich interactively:**
```
/enrich-contacts
```
Claude will ask whether you want single or batch mode.

### Standalone (CLI)

**Single contact:**
```bash
python enrich.py single Amy Chen pilot.com https://www.linkedin.com/in/lihsinchen/
```

**Batch CSV:**
```bash
python enrich.py batch prospects.csv enriched-output.csv
```

If no output path is provided, it defaults to `prospects-enriched.csv`.

## Input CSV Format

Your CSV should include these columns (naming is flexible):

| Column | Required | Notes |
|--------|----------|-------|
| `First Name` | Yes | |
| `Last Name` | Yes | |
| `Full Name` | Optional | Used for display |
| `Company Name` | Optional | Used for display |
| `Company Domain` | Yes | e.g. `pilot.com` — used for alternative suggestions |
| `LinkedIn Profile` | Yes | Full LinkedIn URL — primary lookup key |

## Output

The enriched CSV retains all original columns and adds:

| Column | Description |
|--------|-------------|
| `Email` | Verified work email address |
| `Email Verified` | `Yes` or `No` |
| `All Emails` | All known work emails (semicolon-separated) |
| `Phone` | Direct mobile/phone number |
| `Phone Verified` | `Yes` or `No` |
| `Enrichment Status` | `Complete` / `Email Only` / `Phone Only` / `FLAGGED - No Data Found` |
| `Suggested Alternatives` | Other contacts at the same company (only when flagged) |

## How It Works

1. **Validates your API key** and checks remaining credits
2. **Calls `/v2/enrichment/email`** with each contact's LinkedIn URL
3. **Calls `/v2/enrichment/phone`** with each contact's LinkedIn URL
4. **If both fail**, calls `/v2/search/employee-finder` to suggest up to 3 alternative contacts at the same company
5. **Writes results** to an enriched CSV file

Rate limiting is built in (5 requests/second max).

## API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v2/enrichment/email` | POST | Find verified work email |
| `/v2/enrichment/phone` | POST | Find direct phone number (US only) |
| `/v2/search/employee-finder` | POST | Suggest alternative contacts |
| `/v2/account/key-info` | GET | Check credits and key validity |

## Credits & Costs

- Each contact uses **~2 credits** (1 email + 1 phone lookup)
- Flagged contacts may use 1 additional credit for alternative suggestions
- The script warns you before proceeding if credits are low

## Example Output

```
[1/9] Enriching Amy Chen at Pilot.com...
  Email: amy.chen@pilot.com (Verified: Yes)
  Phone: N/A (Verified: No)
  Status: Email Only

[2/9] Enriching Khalil Snobar at Backblaze...
  Email: ksnobar@backblaze.com (Verified: Yes)
  Phone: +17653377085 (Verified: Yes)
  Status: Complete

==================================================
Enrichment complete!
Output: prospects-enriched.csv
Total: 9 | Emails: 9 | Phones: 5 | Flagged: 0
```

## License

MIT
