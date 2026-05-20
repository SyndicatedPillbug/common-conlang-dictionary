# Kharvunic Workbench v1

This repository contains a modular diachronic conlang workbench for:
- Temple Common
- Boardroom Common
- Trade Common

The system evolves real Romance/Latin roots through ordered sound-change rules while preserving lineage traces and historical auditability.

## Quick Start

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\\Scripts\\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the workbench:

```bash
streamlit run app_v1.py
```

## Main Features

- lineage-aware evolution
- editable rule library
- override management
- IPA rendering
- rhythm/stress analysis
- collision detection
- dictionary history
- source validation
- semantic domains
- export tooling

## Important Design Philosophy

This project does NOT randomly invent words.

Every lexical form should:
1. derive from a real historical Romance/Latin source,
2. evolve through explicit sound/cultural shifts,
3. preserve lineage visibility,
4. support register divergence.

Temple Common preserves:
- liturgical restoration
- poetic cadence
- fossilized forms

Boardroom Common preserves:
- legal precision
- prestige standardization

Trade Common preserves:
- erosion
- compression
- contact-language simplification

## Recommended Workflow

1. Add or validate a source root.
2. Evolve it through one or more registers.
3. Inspect lineage traces.
4. Review collisions.
5. Assign semantic domains.
6. Save into the canonical dictionary.
7. Export as needed.
