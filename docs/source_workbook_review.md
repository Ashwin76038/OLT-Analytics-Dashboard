# Original workbook reconciliation

On 1 October 2026, the project author supplied the original customer/service workbook privately and confirmed that **Activation Date means the date the customer's internet plan/service was activated**. The author identifies a confidential government-platform export and confirms that amounts should be read with their listed plan periods. Portal/billing documents will not be requested or published. Currency, actual snapshot date and A/D/E business definitions remain undisclosed; reference dates and status mappings are analytical assumptions.

## Source scope and comparison

The workbook contains 1,320 service rows. Filtering `Sub Service Type = BHARAT FIBER COMBO` gives 1,280 rows and excludes 40 rows belonging to other service types. The filter explains the project scope; it does not assert those excluded records are invalid. Trimming, lowercasing and collapsing internal whitespace in the private customer labels gives 1,193 groups. The filtered source contains 12 distinct OLT addresses. No labels or addresses are exported by the audit.

| Evidence | Original workbook / selected scope | Current public model |
|---|---|---|
| Activation range | 1999-02-15 through 2026-08-29 | 2025-06-04 through 2028-11-30 |
| Dates after configured 2026-09-12 cutoff | 0 | 810 |
| Matched positional activation dates | 5 of 1,280 | 1,275 differ from source |
| Positional corroboration | Original filtered row order | All 1,280 fees, plan names, OLT groups, customer groups and mapped statuses match |

Both projects' public activation-date sequences are identical. The original workbook supports the date discrepancy, but **does not identify the transformation that caused it**. The currently committed builder only consumes an already prepared customer CSV; the original-to-prepared transformation is not documented. Do not attribute the 810 future public dates to the original source or automatically reinterpret them as renewal/expiry dates.

The comparison is corroborated by row order and other fields, not a verified stable service-ID join. The source codes A/D/E match the existing active/partial-active/inactive mapping in all rows, but this numerical match does not establish their business meaning. The source's 12 distinct address groups do not verify a physical OLT inventory; the author selected ten different OLT IDs for the separate Excel usage simulation.

## Reproduce privately

```bash
python -m pip install -r requirements.txt
python scripts/reconcile_source_workbook.py --source /private/path/original.xlsx
```

The script reads the workbook in memory and emits aggregates only. An optional `--output docs/source_workbook_receipt.json` saves the aggregate receipt. It never modifies the source, public data, keys or Power BI files. A public clone without the private workbook can run public tests/audits, but cannot rerun this private-source comparison.

Executed: the original-workbook comparison above and 13/13 unit tests passed, including explicit day-first parsing, invalid-date rejection, plan-period reconciliation and refusal to force positional date matches when source scope differs. Desktop/DAX execution has not been performed.

## Correction awaiting the approved data/report phase

Use explicit DD/MM/YYYY HH:MM:SS parsing, retain the source timestamp privately, document the Combo-service filter and preserve frozen public keys through a validated mapping. Restore source dates only through an approved, privacy-reviewed rebuild. If the actual snapshot date remains undisclosed, use a clearly labeled analytical reference date and restrict temporal interpretations accordingly. Current public dates and the 810-row quarantine remain in place. Exact dates need privacy review before publication.

The original workbook contains customer labels, emails, addresses and private OLT addresses. It and the attachment screenshot must remain outside Git. The committed receipt contains aggregate evidence only. Power BI execution is still pending the user's approval.
