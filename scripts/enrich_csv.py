"""
GTM Outbound Personalizer - CSV Enrichment Script

Takes a CSV of companies/contacts and adds:
1. Target ICP - concise summary of what the company does
2. Outbound Gap - TRUE/WARM/FALSE classification
3. Target Column - personalized one-liner based on outbound gap

Usage:
    python enrich_csv.py input.csv output.csv
"""

import csv
import re
import sys

# ── Config ───────────────────────────────────────────────────────────────

SECTOR_MAP = {
    'Banking Financial Services': 'financial services',
    'Business Services General': 'business services',
    'Automotive Transport': 'automotive and transport',
    'Construction Renovation': 'construction and renovation',
    'Consulting Advisory': 'consulting and advisory',
    'Consumer Products': 'consumer products',
    'Consumer Services': 'consumer services',
    'Data Processing Hosting': 'data and hosting',
    'Ecommerce': 'ecommerce',
    'Education': 'education',
    'Electronics': 'electronics',
    'Energy': 'energy',
    'Entertainment': 'entertainment',
    'Finance Insurance': 'finance and insurance',
    'Government': 'government',
    'Health': 'healthcare',
    'Hospitality': 'hospitality',
    'Legal Services': 'legal services',
    'Manufacturing': 'manufacturing',
    'Marketing Services': 'marketing services',
    'Media Publishing': 'media and publishing',
    'Medical Wellness': 'medical and wellness',
    'Non Profit': 'non-profit',
    'Oil Gas': 'oil and gas',
    'Real Estate': 'real estate',
    'Retail': 'retail',
    'Shipping': 'shipping and logistics',
    'Technology Hardware Storage': 'technology',
    'Technology Software': 'technology',
    'Architecture': 'architecture',
    'Other': '',
}

SERVICE_PATTERNS = [
    (r'\b(SEO|search engine optimiz\w+)\b', 'SEO'),
    (r'\b(paid (ads|media|search|advertising)|PPC|Google Ads|SEM)\b', 'paid media'),
    (r'\b(content marketing|content strateg\w+)\b', 'content marketing'),
    (r'\b(social media|social marketing)\b', 'social media marketing'),
    (r'\b(email marketing|email automation)\b', 'email marketing'),
    (r'\b(marketing automation)\b', 'marketing automation'),
    (r'\b(web design|website design|web development)\b', 'web design and development'),
    (r'\b(inbound marketing)\b', 'inbound marketing'),
    (r'\b(CRM|customer relationship)\b', 'CRM'),
    (r'\b(HubSpot)\b', 'HubSpot solutions'),
    (r'\b(lead gen\w*)\b', 'lead generation'),
    (r'\b(revenue operations|RevOps)\b', 'RevOps'),
    (r'\b(account.based marketing|ABM)\b', 'ABM'),
    (r'\b(sales enablement)\b', 'sales enablement'),
    (r'\b(conversion (rate )?optimiz\w+|CRO)\b', 'CRO'),
    (r'\b(brand(ing)? strateg\w+|brand development)\b', 'brand strategy'),
    (r'\b(e-?commerce)\b', 'ecommerce'),
    (r'\b(data analytics|analytics|data.driven)\b', 'analytics'),
    (r'\b(digital transformation)\b', 'digital transformation'),
    (r'\b(growth marketing|growth strateg\w+)\b', 'growth marketing'),
    (r'\b(customer experience|CX)\b', 'customer experience'),
]

AUDIENCE_PATTERNS = [
    (r'\bB2B\b', 'B2B'),
    (r'\bB2C\b', 'B2C'),
    (r'\bSaaS\b', 'SaaS'),
    (r'\bstartup\w*\b', 'startups'),
    (r'\benter?prise\b', 'enterprise'),
    (r'\bSMB|small (and medium |& medium )?business\w*\b', 'SMBs'),
    (r'\bmid.?market\b', 'mid-market companies'),
    (r'\bmanufactur\w+\b', 'manufacturers'),
    (r'\bhealthcare|medical\b', 'healthcare companies'),
    (r'\bfinancial|fintech\b', 'financial services'),
    (r'\btechnology|tech compan\w+\b', 'technology companies'),
    (r'\be-?commerce\b', 'ecommerce brands'),
]

OUTBOUND_KEYWORDS = [
    'outbound', 'sdr', 'cold email', 'cold calling', 'sales development',
    'appointment setting', 'meeting booking', 'booked meetings',
    'business development representative', 'cold outreach',
    'appointment generation', 'outreach campaign',
]

LEADGEN_KEYWORDS = [
    'lead gen', 'lead generation', 'demand gen', 'demand generation',
    'prospecting', 'pipeline generation', 'appointment',
]

DETECT_SERVICES = [
    ('seo', 'SEO'), ('paid ads', 'paid ads'), ('paid media', 'paid media'),
    ('ppc', 'PPC'), ('content marketing', 'content marketing'),
    ('inbound marketing', 'inbound marketing'), ('inbound', 'inbound'),
    ('crm', 'CRM'), ('hubspot', 'HubSpot'), ('web design', 'web design'),
    ('website design', 'web design'), ('social media', 'social media'),
    ('email marketing', 'email marketing'), ('automation', 'automation'),
    ('branding', 'branding'), ('analytics', 'analytics'),
    ('revops', 'RevOps'), ('revenue operations', 'RevOps'),
    ('abm', 'ABM'), ('lead gen', 'lead gen'), ('demand gen', 'demand gen'),
    ('outbound', 'outbound'), ('sdr', 'SDR services'),
    ('cold email', 'cold email'), ('appointment setting', 'appointment setting'),
    ('prospecting', 'prospecting'), ('sales development', 'sales development'),
]


# ── Helpers ──────────────────────────────────────────────────────────────

def clean(text):
    text = re.sub(r'[➤→►▸●•✅⭐💡📞✔️🏆🔥🚀❤️✨💪🎯🌍🌎🏅👉]+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_services(description):
    services = []
    seen = set()
    for pattern, label in SERVICE_PATTERNS:
        if label not in seen and re.search(pattern, description, re.IGNORECASE):
            services.append(label)
            seen.add(label)
        if len(services) >= 3:
            break
    return services


def extract_audience(description, b2b_b2c):
    audiences = []
    seen = set()
    for pattern, label in AUDIENCE_PATTERNS:
        if label not in seen and re.search(pattern, description, re.IGNORECASE):
            audiences.append(label)
            seen.add(label)
        if len(audiences) >= 2:
            break
    if not audiences and b2b_b2c:
        audiences.append(b2b_b2c.strip())
    return audiences


def extract_what_they_do(description, company):
    desc = clean(description)
    desc = re.sub(re.escape(company), '', desc, flags=re.IGNORECASE).strip()
    patterns = [
        (r'help(?:s|ing)?\s+(.{15,80}?)(?:\.|$)', True),
        (r'specializ\w+\s+in\s+(.{10,80}?)(?:\.|$)', False),
        (r'focus\w*\s+on\s+(.{10,80}?)(?:\.|$)', False),
        (r'(?:we )?provid\w+\s+(.{10,80}?)(?:\.|$)', False),
        (r'(?:we )?deliver\w*\s+(.{10,80}?)(?:\.|$)', False),
        (r'(?:we )?offer\w*\s+(.{10,80}?)(?:\.|$)', False),
    ]
    for pat, prefix_helping in patterns:
        m = re.search(pat, desc, re.IGNORECASE)
        if m:
            result = m.group(1).strip()
            result = re.sub(r'\s+(through|by|via|using|with|for)\s*$', '', result)
            if result.lower().startswith('you'):
                continue
            if len(result) > 15:
                if prefix_helping:
                    return 'helping ' + result
                return result
    return ''


def _bad_phrase(text):
    t = text.lower().strip()
    bad_starts = ['that', 'this', 'it ', 'our ', 'your ', 'my ', 'first ', 'the most',
                  'why ', 'how ', 'what ', 'when ', 'where ', 'which ']
    if any(t.startswith(b) for b in bad_starts):
        return True
    if ' you ' in t or t.startswith('you'):
        return True
    if re.search(r'\b(by|around|of|to|the|a|an|and|or|but|in|on|at|for|with|from),?\s*$', t):
        return True
    return False


def make_target_icp(company, description, sector, service_col, b2b_b2c):
    desc = clean(description)
    clean_sector = SECTOR_MAP.get(sector.strip(), sector.lower().strip())
    services = extract_services(desc)
    audiences = extract_audience(desc, b2b_b2c)
    what_they_do = extract_what_they_do(desc, company)

    if services:
        if len(services) >= 2:
            svc_phrase = ', '.join(services[:-1]) + ' and ' + services[-1]
        else:
            svc_phrase = services[0]
        if audiences and audiences[0] not in ('B2B', 'B2C'):
            icp = f"{svc_phrase} for {audiences[0]}"
        elif clean_sector and clean_sector not in svc_phrase.lower():
            icp = f"{svc_phrase} in the {clean_sector} space"
        elif audiences:
            icp = f"{svc_phrase} for {audiences[0]} companies"
        else:
            icp = svc_phrase
    elif what_they_do and not _bad_phrase(what_they_do):
        icp = what_they_do
        if len(icp) > 80:
            icp = icp[:77].rsplit(' ', 1)[0]
    else:
        svc_summary = ''
        if '|' in service_col:
            svc_summary = service_col.split('|', 1)[1].strip()
        if svc_summary:
            svc_summary = re.sub(r'^(We |They |' + re.escape(company) + r'\s*(is|are)\s*)', '', svc_summary, flags=re.IGNORECASE)
            svc_summary = re.sub(r'^(a |an |the )', '', svc_summary, flags=re.IGNORECASE)
            if len(svc_summary) > 80:
                svc_summary = svc_summary[:77].rsplit(' ', 1)[0]
            if not _bad_phrase(svc_summary):
                icp = svc_summary
            elif clean_sector:
                icp = f"digital solutions for the {clean_sector} sector"
            else:
                icp = "digital marketing and growth"
        elif clean_sector:
            icp = f"digital solutions for the {clean_sector} sector"
        else:
            icp = "digital marketing and growth"

    icp = icp.strip().rstrip('.')
    icp = re.sub(r'\bhubspot\b', 'HubSpot', icp, flags=re.IGNORECASE)
    if icp and icp[0].isupper():
        first_word = icp.split()[0]
        if not (first_word.isupper() and len(first_word) <= 5) and first_word != 'HubSpot':
            icp = icp[0].lower() + icp[1:]
    if len(icp) > 100:
        icp = icp[:97].rsplit(' ', 1)[0]
    return icp


def classify_outbound_gap(description, service_col):
    combined = (description + ' ' + service_col).lower()
    has_outbound = any(kw in combined for kw in OUTBOUND_KEYWORDS)
    has_leadgen = any(kw in combined for kw in LEADGEN_KEYWORDS)
    if has_outbound:
        return 'FALSE'
    elif has_leadgen:
        return 'WARM'
    else:
        return 'TRUE'


def detect_services_for_column(description):
    desc_lower = description.lower()
    found = []
    seen = set()
    for keyword, label in DETECT_SERVICES:
        if keyword in desc_lower and label not in seen:
            found.append(label)
            seen.add(label)
    return found


def build_target_column(company, description, outbound_gap):
    services = detect_services_for_column(description)
    specific = [s for s in services if s not in ('HubSpot', 'CRM', 'automation', 'analytics', 'inbound')]
    if not specific:
        specific = [s for s in services if s not in ('HubSpot',)]

    if len(specific) >= 3:
        svc_text = f"{specific[0]}, {specific[1]} and {specific[2]}"
    elif len(specific) == 2:
        svc_text = f"{specific[0]} and {specific[1]}"
    elif len(specific) == 1:
        svc_text = specific[0]
    else:
        svc_text = ''

    if outbound_gap == 'TRUE':
        if svc_text:
            return f"I can see {company} covers {svc_text} but I didn't see anything around outbound or booked meetings for clients"
        else:
            return f"I noticed {company} doesn't seem to offer outbound or booked meetings as part of the service stack"
    elif outbound_gap == 'WARM':
        warm = [s for s in services if s in ('lead gen', 'demand gen', 'prospecting', 'ABM')]
        if warm:
            return f"I can see {company} already does {warm[0]} which means you get the problem. The gap I keep seeing is turning those leads into actual booked meetings"
        elif svc_text:
            return f"I noticed {company} already does {svc_text} and some lead gen. Most partners in that position just need the last mile to get clients booked meetings"
        else:
            return f"I can see {company} already touches lead gen. The piece most partners are missing is turning those leads into booked calls on the calendar"
    elif outbound_gap == 'FALSE':
        out = [s for s in services if s in ('outbound', 'SDR services', 'cold email', 'appointment setting', 'sales development')]
        if out:
            return f"I can see {company} already offers {out[0]} so you know how hard it is to scale that across multiple clients without the ops falling apart"
        else:
            return f"I noticed {company} already does some outbound. Most agencies in that position hit a ceiling when they try to scale it past a handful of clients"

    return f"I took a look at what {company} offers and it seems like outbound could be a natural add to the stack"


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python enrich_csv.py input.csv [output.csv]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.csv', '_enriched.csv')

    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    print(f"Processing {len(rows)} rows...")

    # Detect column indices (flexible mapping)
    col_map = {}
    for i, h in enumerate(header):
        hl = h.lower().strip()
        if 'company' in hl and ('name' in hl or 'table' in hl or 'data' in hl):
            col_map['company'] = i
        elif 'description' in hl or 'desc' in hl or 'bio' in hl:
            col_map['description'] = i
        elif 'sector' in hl or 'industry' in hl:
            col_map['sector'] = i
        elif 'first' in hl and 'name' in hl:
            col_map['firstname'] = i
        elif 'service' in hl and 'client' not in hl and 'b2b' not in hl:
            col_map['service'] = i
        elif 'b2b' in hl or 'b2c' in hl:
            col_map['b2b_b2c'] = i

    print(f"Column mapping: {col_map}")

    header.extend(['Target ICP', 'Outbound Gap', 'Target Column'])

    true_c = warm_c = false_c = 0

    for row in rows:
        company = row[col_map.get('company', 1)].strip() if col_map.get('company', 1) < len(row) else ''
        description = row[col_map.get('description', 3)] if col_map.get('description', 3) < len(row) else ''
        sector = row[col_map.get('sector', 4)] if col_map.get('sector', 4) < len(row) else ''
        service_col = row[col_map.get('service', 16)] if col_map.get('service', 16) < len(row) else ''
        b2b_b2c = row[col_map.get('b2b_b2c', 17)] if col_map.get('b2b_b2c', 17) < len(row) else ''

        # Capitalize first name
        fn_idx = col_map.get('firstname', 5)
        if fn_idx < len(row) and row[fn_idx].strip():
            row[fn_idx] = row[fn_idx].strip().title()

        # Generate columns
        icp = make_target_icp(company, description, sector, service_col, b2b_b2c)
        gap = classify_outbound_gap(description, service_col)
        tc = build_target_column(company, description, gap)

        row.extend([icp, gap, tc])

        if gap == 'TRUE': true_c += 1
        elif gap == 'WARM': warm_c += 1
        else: false_c += 1

    print(f"\nWriting {output_file}...")
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    total = len(rows)
    print(f"\nDone! {total} rows enriched.")
    print(f"\nOUTBOUND GAP BREAKDOWN:")
    print(f"  TRUE  (pure gap):     {true_c:>5} ({true_c*100//total}%)")
    print(f"  WARM  (has lead gen): {warm_c:>5} ({warm_c*100//total}%)")
    print(f"  FALSE (has outbound): {false_c:>5} ({false_c*100//total}%)")
    print(f"\nOutput: {output_file}")


if __name__ == '__main__':
    main()
