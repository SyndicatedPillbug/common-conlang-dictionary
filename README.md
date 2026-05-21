# Common Conlang Dictionary

A diachronic language workbench for evolving Romance/Latin roots into:

- Temple Common (Kharvūnic)
- Boardroom Common
- Trade Common

The goal is reproducible linguistic evolution rather than ad hoc word invention. The default app path is now the consolidated v2 workbench.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate with:

```bash
.venv\\Scripts\\activate
```

## Run the v2 workbench

```bash
streamlit run app.py
```

`app.py` is the primary user-facing entry point. It uses `EvolutionEngineV2` by default and includes the complete v2 workflow:

1. evolve one word with visible diagnostics,
2. inspect full lineage with rule IDs and explanations,
3. compare Temple, Boardroom, and Trade forms side by side,
4. save complete dictionary entries with collision warnings and history, while blocking weak/failing candidates from canonical save,
5. run the diagnostic root corpus and inspect root health.

Legacy/development launchers remain in the repository for reference only:

- `app_v1.py`
- `app_v2.py`
- `app_workbench.py`
- `app_launcher.py`

Do not treat those files as the primary app path.

## Test

```bash
python -m pytest
```

The test suite includes guards for the previous fake-success failure modes: `ambulare` must not silently return `ambulare`, and weak/failing candidates must not be canonical-saveable.
 
## Structure

- `app.py` — consolidated Streamlit v2 workbench
- `kharvunic/evolution_v2.py` — serious v2 evolution engine
- `kharvunic/diagnostics.py` — unchanged/weak/failing evolution diagnostics
- `kharvunic/diagnostic_runner.py` — corpus-level root health checks
- `kharvunic/workflows.py` — v2 save workflow and dictionary persistence
- `data/rules_v2.csv` — richer staged sound-change rule library
- `data/diagnostic_roots.csv` — diagnostic root corpus
- `data/dictionary.csv` — canonical dictionary
- `data/dictionary_history.csv` — audit trail for saved entries

## Example

Input:

```text
ambulare
walk
temple
```

The app should show visible lineage: `ambulare → amvulare → amvular → amvulār`. It should never silently present an unchanged source form, or a weak candidate, as a successful canonical result.

Input:

```text
misericordia
mercy
```

The Compare Registers page shows Temple, Boardroom, and Trade outputs together, with diagnostics for each register.
