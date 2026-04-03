# HubSpot Partner Outbound Sequence - 5 Emails

## Variables
- `{{firstName}}` - first name
- `{{companyName}}` - agency name
- `{{targeticp}}` - what the agency does / who they serve
- `{{targetcolumn}}` - personalized outbound gap line (TRUE/WARM/FALSE aware)
- `{a|b|c}` - spintax rotation
- `%signature%` - signature block

## Segments (Outbound Gap column)
- **TRUE** (7,633 / 93%) - no outbound or lead gen at all
- **WARM** (439 / 5%) - does lead gen but no outbound
- **FALSE** (76 / 1%) - already claims outbound/SDR

---

# EMAIL 1 - Day 1 (A/B split)

## Variant A

**Subject:** `{outbound gap|client pipeline|meetings for clients}`

{{firstName}}, most HubSpot partners I speak to only offer inbound and CRM.

{{targetcolumn}}.

When a client asks for booked meetings, what does {{companyName}} tell them today?

We bolt outbound systems onto your HubSpot stack so clients get pipeline without you building an SDR team from scratch.

Same systems that helped grow Push to $30M ARR bootstrapped.

{Worth exploring?|Is this on your radar?|Something you've thought about?}

{All the best,|Cheers,|Best,} %signature%

{P.S. If this isn't a need, just let me know and I won't follow up.|P.S. If this isn't top of mind, just let me know and I won't follow up.|P.S. If this isn't relevant, just tell me and I won't follow up.}

---

## Variant B

**Subject:** `{quick question|{{companyName}} + outbound|pipeline gap}`

{{firstName}}, I keep having the same conversation with HubSpot partners.

{{targetcolumn}}.

Clients love the CRM. They like the reports. Then someone asks "so where are the actual meetings?"

We plug a done-for-you outbound system right into your clients' HubSpot. Your brand, your client, our engine.

{Curious if this has come up for {{companyName}}?|Has this come up at {{companyName}}?|Something you've run into?}

{All the best,|Cheers,|Best,} %signature%

{P.S. If this isn't relevant, just say the word and I'll back off.|P.S. Not a fit? Just let me know and I won't follow up.|P.S. If the timing is off, just tell me and I'll leave it.}

---
---

# EMAIL 2 - Day 3 (A/B split)

## Variant A

**Subject:** `{re: outbound|one more thing}`

{{firstName}}, just wanted to add some context to my last note.

The number one reason HubSpot clients leave their agency isn't bad work. It's that inbound alone doesn't fill a sales calendar fast enough.

Outbound fixes that {from month one|in weeks not quarters}. We run sequenced email and LinkedIn through your clients' HubSpot. Booked calls not just contacts. All under your brand.

No SDR hires. No new tools. {You don't change your stack at all.|Nothing changes on your side.}

{Worth a quick chat?|Want to see how it works?|Open to a 10 min walkthrough?}

{All the best,|Cheers,|Best,} %signature%

---

## Variant B

**Subject:** `{the numbers on this|new revenue line}`

{{firstName}}, wanted to put some real numbers behind my last note.

You add outbound as a managed service to {3|4|5} existing clients. We run cold email and LinkedIn through their HubSpot. Each client gets {15-30|20-40} qualified meetings a month on their calendar. You charge a retainer on top.

No new hires. No cold calling. Everything runs inside HubSpot so reporting stays clean.

Same setup helped one partner turn this into their {fastest growing|most profitable} service line last quarter.

{Interested in seeing the playbook?|Want me to walk you through it?|Worth a look?}

{All the best,|Cheers,|Best,} %signature%

---
---

# EMAIL 3 - Day 7 (single variant, breakup)

**Subject:** `{closing the loop|should I close this out?|last note}`

{{firstName}}, I've reached out a couple times about adding outbound to what {{companyName}} already offers. Totally understand if {the timing is off|this isn't a priority|it's not the right fit right now}.

If it ever comes up. A client asking for meetings, pipeline gaps, or you just want a new revenue line without adding headcount. {I'm easy to find.|Happy to chat whenever.|You know where to find me.}

{No hard feelings either way.|All good either way.|Appreciate your time regardless.}

{Cheers,|Best,|All the best,} %signature%

---
---

# HOW EMAIL 1 VARIANT A LANDS

## TRUE (93%)

Disha, most HubSpot partners I speak to only offer inbound and CRM.

I can see Insidea covers RevOps but I didn't see anything around outbound or booked meetings for clients.

When a client asks for booked meetings, what does Insidea tell them today?

We bolt outbound systems onto your HubSpot stack so clients get pipeline without you building an SDR team from scratch.

Same systems that helped grow Push to $30M ARR bootstrapped.

Worth exploring?

Cheers, %signature%

P.S. If this isn't a need, just let me know and I won't follow up.

---

## WARM (5%)

Neil, most HubSpot partners I speak to only offer inbound and CRM.

I can see NP Digital already does lead gen which means you get the problem. The gap I keep seeing is turning those leads into actual booked meetings.

When a client asks for booked meetings, what does NP Digital tell them today?

We bolt outbound systems onto your HubSpot stack so clients get pipeline without you building an SDR team from scratch.

Same systems that helped grow Push to $30M ARR bootstrapped.

Is this on your radar?

Best, %signature%

P.S. If this isn't top of mind, just let me know and I won't follow up.

---

## FALSE (1%)

Conor, most HubSpot partners I speak to only offer inbound and CRM.

I noticed Uptown Creation already does some outbound. Most agencies in that position hit a ceiling when they try to scale it past a handful of clients.

When a client asks for booked meetings, what does Uptown Creation tell them today?

We bolt outbound systems onto your HubSpot stack so clients get pipeline without you building an SDR team from scratch.

Same systems that helped grow Push to $30M ARR bootstrapped.

Something you've thought about?

All the best, %signature%

P.S. If this isn't relevant, just tell me and I won't follow up.

---
---

# SENDING STRATEGY

| Setting | Recommendation |
|---|---|
| **Step 1** | A/B split 50/50. No links, no images, no tracking pixel. |
| **Step 2** | A/B split 50/50. Can add calendar link. Enable open tracking. |
| **Step 3** | Single variant. Keep short. Optional calendar link. |
| **Timing** | Day 1, Day 3, Day 7 |
| **Daily volume** | Ramp 20/day/inbox to 50/day/inbox over 2 weeks |
| **Inboxes** | 3-5 minimum, rotate across sends |
| **Warmup** | 2 weeks before launch, keep running during campaign |
| **Dedupe** | One contact per company domain (pick Founder > CEO > Director) |
| **Language** | Remove rows with non-English descriptions before uploading |
| **Segments** | Upload TRUE (7,633) first. WARM (439) second. Skip FALSE (76) or run manually. |
