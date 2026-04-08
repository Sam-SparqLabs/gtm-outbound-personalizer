import csv
import json
import sys
import time
import urllib.request

API_KEY = "blitz-019d6d8d-ec05-7e4b-a339-ff92f8b42a67"
BASE_URL = "https://api.blitz-api.ai/v2"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
}


def api_post(endpoint, payload):
    url = f"{BASE_URL}{endpoint}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        print(f"  API error {e.code} on {endpoint}: {body}", file=sys.stderr)
        return {"found": False}


def api_get(endpoint):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        print(f"  API error {e.code} on {endpoint}: {body}", file=sys.stderr)
        return {}


def find_email(linkedin_url):
    return api_post("/enrichment/email", {"person_linkedin_url": linkedin_url})


def find_phone(linkedin_url):
    return api_post("/enrichment/phone", {"person_linkedin_url": linkedin_url})


def suggest_alternatives(company_domain):
    try:
        result = api_post("/search/employee-finder", {"company_domain": company_domain, "limit": 3})
        if isinstance(result, list):
            return result
        return result.get("results", result.get("employees", []))
    except Exception as e:
        print(f"  Employee finder error: {e}", file=sys.stderr)
        return []


def check_credits():
    info = api_get("/account/key-info")
    if not info.get("valid"):
        print("ERROR: Invalid API key.", file=sys.stderr)
        sys.exit(1)
    credits = info.get("remaining_credits", 0)
    print(f"API key valid. Credits remaining: {credits}")
    return credits


def enrich_single(first_name, last_name, company_domain, linkedin_url=None):
    """Enrich a single contact. Returns a dict with results."""
    full_name = f"{first_name} {last_name}"
    result = {
        "Full Name": full_name,
        "Company Domain": company_domain,
        "Email": "",
        "Email Verified": "No",
        "All Emails": "",
        "Phone": "",
        "Phone Verified": "No",
        "Enrichment Status": "",
        "Suggested Alternatives": "",
    }

    if not linkedin_url:
        print(f"  No LinkedIn URL for {full_name}, skipping.")
        result["Enrichment Status"] = "FLAGGED - No LinkedIn URL"
        return result

    email_result = find_email(linkedin_url)
    time.sleep(0.25)
    phone_result = find_phone(linkedin_url)
    time.sleep(0.25)

    email_found = email_result.get("found", False)
    phone_found = phone_result.get("found", False)

    result["Email"] = email_result.get("email", "")
    result["Email Verified"] = "Yes" if email_found else "No"

    all_emails = email_result.get("all_emails", [])
    result["All Emails"] = "; ".join(e.get("email", "") for e in all_emails) if all_emails else ""

    result["Phone"] = phone_result.get("phone") or ""
    result["Phone Verified"] = "Yes" if phone_found else "No"

    if email_found and phone_found:
        result["Enrichment Status"] = "Complete"
    elif email_found:
        result["Enrichment Status"] = "Email Only"
    elif phone_found:
        result["Enrichment Status"] = "Phone Only"
    else:
        result["Enrichment Status"] = "FLAGGED - No Data Found"
        if company_domain:
            time.sleep(0.25)
            alts = suggest_alternatives(company_domain)
            if alts:
                alt_strs = []
                for a in alts[:3]:
                    alt_name = a.get("full_name", a.get("name", "Unknown"))
                    alt_title = a.get("title", a.get("job_title", ""))
                    alt_strs.append(f"{alt_name} ({alt_title})")
                result["Suggested Alternatives"] = "; ".join(alt_strs)

    return result


def enrich_csv(input_file, output_file):
    """Enrich all contacts in a CSV file."""
    rows = []
    with open(input_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        original_fields = list(reader.fieldnames)
        for row in reader:
            rows.append(row)

    credits = check_credits()
    estimated_cost = len(rows) * 2
    print(f"Contacts to enrich: {len(rows)} (estimated credits: {estimated_cost})")

    if credits < estimated_cost:
        print(f"WARNING: May not have enough credits ({credits} remaining, ~{estimated_cost} needed)")

    enriched_fields = original_fields + [
        "Email", "Email Verified", "All Emails",
        "Phone", "Phone Verified",
        "Enrichment Status", "Suggested Alternatives",
    ]

    enriched_rows = []
    request_count = 0

    for i, row in enumerate(rows):
        name = row.get("Full Name", row.get("First Name", "Unknown"))
        company = row.get("Company Name", "Unknown")
        linkedin = row.get("LinkedIn Profile", row.get("LinkedIn URL", ""))
        domain = row.get("Company Domain", "")

        print(f"\n[{i+1}/{len(rows)}] Enriching {name} at {company}...")

        if request_count >= 4:
            time.sleep(1)
            request_count = 0

        result = enrich_single(
            row.get("First Name", ""),
            row.get("Last Name", ""),
            domain,
            linkedin,
        )
        request_count += 2

        row.update(result)
        enriched_rows.append(row)

        print(f"  Email: {row['Email'] or 'N/A'} (Verified: {row['Email Verified']})")
        print(f"  Phone: {row['Phone'] or 'N/A'} (Verified: {row['Phone Verified']})")
        print(f"  Status: {row['Enrichment Status']}")

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=enriched_fields)
        writer.writeheader()
        writer.writerows(enriched_rows)

    total = len(enriched_rows)
    email_count = sum(1 for r in enriched_rows if r["Email Verified"] == "Yes")
    phone_count = sum(1 for r in enriched_rows if r["Phone Verified"] == "Yes")
    flagged = sum(1 for r in enriched_rows if "FLAGGED" in r["Enrichment Status"])

    print(f"\n{'='*50}")
    print(f"Enrichment complete!")
    print(f"Output: {output_file}")
    print(f"Total: {total} | Emails: {email_count} | Phones: {phone_count} | Flagged: {flagged}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Single:  python enrich.py single <first> <last> <domain> [linkedin_url]")
        print("  Batch:   python enrich.py batch <input.csv> [output.csv]")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "single":
        if len(sys.argv) < 5:
            print("Usage: python enrich.py single <first> <last> <domain> [linkedin_url]")
            sys.exit(1)
        check_credits()
        first = sys.argv[2]
        last = sys.argv[3]
        domain = sys.argv[4]
        linkedin = sys.argv[5] if len(sys.argv) > 5 else None
        result = enrich_single(first, last, domain, linkedin)
        print(json.dumps(result, indent=2))

    elif mode == "batch":
        if len(sys.argv) < 3:
            print("Usage: python enrich.py batch <input.csv> [output.csv]")
            sys.exit(1)
        input_file = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else input_file.replace(".csv", "-enriched.csv")
        enrich_csv(input_file, output_file)

    else:
        print(f"Unknown mode: {mode}. Use 'single' or 'batch'.")
        sys.exit(1)
