# Kharvunic Workbench v2

This repository contains a diachronic conlang workbench for:

- Temple Common
- Boardroom Common
- Trade Common

The system evolves real Romance/Latin roots through ordered sound-change rules while preserving lineage traces, register divergence, diagnostics, dictionary persistence, and historical auditability.

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

```bash
.venv\\Scripts\\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the v2 workbench:

```bash
streamlit run app.py
```

Run tests:

```bash
python -m pytest
```

## Main v2 Workflows

The default `app.py` workbench supports five end-to-end workflows.

1. Evolve a word with `EvolutionEngineV2`, including loud warnings for unchanged or weakly changed forms.
2. Inspect full lineage with each intermediate form, rule ID, and rule explanation.
3. Compare Temple, Boardroom, and Trade outputs side by side with diagnostics for each register.
4. Save complete dictionary entries: final form, IPA, register, meaning, source root, semantic domain, notes, and history entry.
5. Run the diagnostic root corpus and view root health as passing, weak, or failing.

## Legacy Launchers

The following files are retained only for legacy or development reference:
- `app_v1.py`
- `app_v2.py`
- `app_workbench.py`
- `app_launcher.py`

The primary launch command is always:

```bash
streamlit run app.py
```

## Important Design Philosophy

This project does not randomly invent words.

Every lexical form should:

1. derive from a real historical Romance/Latin source,
2. evolve through explicit sound/cultural shifts,
3. preserve lineage visibility,
4. support register divergence,
5. expose diagnostics when the rule system is weak.

Temple Common preserves liturgical restoration, poetic cadence, and fossilized forms.

Boardroom Common preserves legal precision and prestige standardization.

Trade Common preserves erosion, compression, and contact-language simplification.

## Recommended Workflow

1. Enter or validate a source root.
2. Evolve it through one register or compare all registers.
3. Inspect lineage and diagnostic health.
4. Review exact and near collisions.
5. Assign a semantic domain and notes.
6. Save into the canonical dictionary.
7. Use diagnostics to improve rules systematically.
