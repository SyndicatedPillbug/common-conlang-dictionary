# Cleanup Target

This repository has accumulated several launcher and engine layers while the language model was being explored.

The intended clean direction is now:

```bash
streamlit run app.py
```

`app.py` should be the only primary application entrypoint.

## Prioritized Current Model

The latest and preferred linguistic model is the v3 epochal model:

- `kharvunic/evolution_v3.py`
- `kharvunic/fractal.py`
- `data/epochs_v3.csv`
- `data/loan_strata_v3.csv`
- `EVOLUTION_MODEL_V3.md`

The old flat-regex v1/v2 approach is useful as prior work, but it should no longer drive the main app.

## Keep

Keep these as active production files:

- `app.py`
- `kharvunic/evolution_v3.py`
- `kharvunic/fractal.py`
- `kharvunic/diagnostics.py`
- `kharvunic/diagnostic_runner.py`
- `kharvunic/workflows.py`
- `kharvunic/history.py`
- `kharvunic/collision.py`
- `kharvunic/domains.py`
- `kharvunic/ipa.py`
- `data/dictionary.csv`
- `data/dictionary_history.csv`
- `data/diagnostic_roots.csv`
- `data/epochs_v3.csv`
- `data/loan_strata_v3.csv`
- `data/semantic_domains.csv`
- `tests/`

## Legacy / Candidate for Deletion or Archive

These should be archived under `legacy/` or deleted after confirming no imports remain:

- `app_v1.py`
- `app_workbench.py`
- `app_launcher.py`
- `app_v2.py` if present
- `app_v3.py` if present
- `app_v3_shell.py` if present
- old UI pages that are not imported by `app.py`
- old `kharvunic/evolution.py`
- old `kharvunic/evolution_v2.py` once v3 tests are stable
- old `data/rules.csv` and `data/rules_v2.csv` if no longer used by production paths

## Cleanup Rule

Do not delete the old files blindly. First run:

```bash
grep -R "evolution_v2\|app_v1\|app_workbench\|app_launcher" -n .
python -m pytest
```

Then archive unused files in a single cleanup commit.

## Definition of Done

The cleanup is done when:

- `streamlit run app.py` launches the complete workbench
- `mañana` no longer becomes `mañan` as a false-success candidate
- diagnostics use `EvolutionEngineV3`
- save workflow uses v3 result fields
- `python -m pytest` passes
- README points only to `app.py`
