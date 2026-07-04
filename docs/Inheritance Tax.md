# Inheritance Tax

How the tool estimates Thai inheritance tax and suggests planning. Implemented in
`tax.py` (see [[Architecture]]). Not tax advice — see [[Disclaimer]]. Related:
[[Asset Sheet]], [[Tips]], [[Thai Estate Law]].

## The rules (Inheritance Tax Act B.E. 2558 / 2015)

- Tax applies to the value each **beneficiary** receives **above 100,000,000 THB** —
  and only to the **excess**, not the whole inheritance.
- **Rate:** 5% for descendants/ascendants (children, parents); 10% for other heirs.
- **Spouses are fully exempt.**
- Inherited assets are **exempt from personal income tax** — the inheritance tax
  regime applies instead.

## Lifetime gift tax (Revenue Code)

- Gifts to ascendants, descendants, or a spouse: exempt up to **20,000,000 THB/year**.
- Gifts to others: exempt up to **10,000,000 THB/year**.
- Amounts above the annual exemption are taxed at **5%**.

## Planning levers the tool surfaces

- The 100M allowance is **per beneficiary** — distributing assets among more
  beneficiaries can reduce or remove tax.
- Routing assets through an **exempt spouse** can defer or avoid tax.
- **Lifetime gifting** within the annual exemptions shrinks the taxable estate.

## Valuation

For land and buildings the value is generally the **official government appraised
value (ราคาประเมินราชการ)**, usually lower than market price — look it up at
<https://assessprice.treasury.go.th>. This is one of the [[Tips]] and appears in the
Asset Inventory document; see [[Asset Sheet]].

## Thresholds in code

`tax.py` constants: `TAX_THRESHOLD_THB = 100_000_000`,
`TAX_RATE_DESCENDANT_ASCENDANT = 0.05`, `TAX_RATE_OTHER = 0.10`,
`GIFT_EXEMPT_LINEAL_THB = 20_000_000`, `GIFT_EXEMPT_OTHER_THB = 10_000_000`. If the
law changes, update these (and the tests) — see [[Development]].
