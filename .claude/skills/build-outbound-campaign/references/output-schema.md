# Output Schema

## Minimum Deliverables

1. Cleaned master CSV
2. Sequencer variable mapping
3. Copy doc with:
   - longer working version
   - final tighter version
   - rendered examples
4. Spintax file with:
   - 2 variants for Email 1
   - 2 variants for Email 2
   - 1 variant for Email 3

## Suggested File Names

- `*_master_cleaned_enriched.csv`
- `*_master_cleaned_enriched_v2.csv`
- `*_Copy.docx`
- `*_Sequencer_Spintax_Variants.md`

## Safety Notes

Always report:
- total rows
- reachable rows
- safe rows
- mismatch-review rows
- missing rows
- remaining Blitz credits after enrichment if checked

## Sequencer Mapping

When the CSV has spaces in column names, tell the user to either:
- map the exact headers directly, or
- create alias fields without spaces inside the sequencer

## Final Handoff

The final handoff should include exact file paths and any caveats about send safety.
