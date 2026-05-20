# Common Conlang Dictionary

A diachronic language engine for evolving Romance/Latin roots into:

- Temple Common (Kharvūnic)
- Boardroom Common
- Trade Common

The goal is reproducible linguistic evolution rather than ad hoc word invention.

## Structure

- `kharvunic/engine.py` — evolution engine
- `kharvunic/rules.py` — sound/cultural shifts
- `data/roots.csv` — source etymologies
- `data/overrides.csv` — liturgical and prestige overrides
- `app.py` — Streamlit GUI

## Example

Input:

`misericordia`

Possible outputs:

- Temple Common: `mezhera`
- Boardroom Common: `mezhr`
- Trade Common: `mej`
