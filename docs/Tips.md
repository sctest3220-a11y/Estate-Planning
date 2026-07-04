# Tips

The general tips/reminders the tool surfaces on the results page and in the CLI.
Implemented in `tips.py` (see [[Architecture]]). Not legal/tax advice — see
[[Disclaimer]].

## Always shown

- **Where the documents live** — tell your executor and family where the signed
  originals are kept; give your hospital and healthcare proxy a copy of the living
  will and medical POA.
- **Keep documents current** — review after marriage, divorce, a new child, buying
  or selling property, or moving country, and re-date them.
- **Bank accounts freeze on death** — Thai accounts are generally frozen until the
  estate is administered; keep an emergency fund someone can reach.
- **Beneficiary designations pass outside the will** — life insurance and some
  provident/retirement funds go to the named beneficiary; keep them current.
- **Keep the asset inventory updated** — see [[Asset Sheet]].

## Conditional tips

- **Land/condo valuation** (when you own real estate) — value by ราคาประเมินราชการ at
  <https://assessprice.treasury.go.th>. See [[Inheritance Tax]].
- **Foreign assets** (non-Thai nationals / foreign will) — keep a matching
  home-country will with a carve-out clause. See [[Thai Estate Law]].
- **Financial power of attorney** (anyone with Thai dealings) — banks and government
  offices usually require the standardized **Tor Dor 21 (ตด.21)** form, not a custom
  POA, and Thai POAs are transaction-specific. The tool can't generate the official
  form, so this is surfaced as guidance.
- **Digital assets** (when a crypto/digital asset is listed) — securely record how
  to access wallets and accounts and leave instructions for your executor.

## Adding tips

Extend `planning_tips(plan)` in `tips.py` and add a case to `tests/test_tips.py`.
Keep them informational and consistent with the [[Disclaimer]].
