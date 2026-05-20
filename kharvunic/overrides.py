"""Override management for deliberate irregular forms.

Overrides are not mistakes. They model:
- liturgical restoration
- poetic preservation
- fossilized forms
- prestige standardization
- Trade Common erosion beyond normal rules

Every override must carry a reason so the language remains auditable.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

OVERRIDE_COLUMNS = [
    'root',
    'register',
    'override',
    'reason',
]

OVERRIDE_PATH = Path('data/overrides.csv')


def ensure_override_file(path: Path = OVERRIDE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        pd.DataFrame(columns=OVERRIDE_COLUMNS).to_csv(path, index=False)


def load_overrides(path: Path = OVERRIDE_PATH) -> pd.DataFrame:
    ensure_override_file(path)
    df = pd.read_csv(path).fillna('')
    missing = set(OVERRIDE_COLUMNS) - set(df.columns)
    assert not missing, f'Override file missing columns: {sorted(missing)}'
    return df[OVERRIDE_COLUMNS]


def find_override(root: str, register: str, path: Path = OVERRIDE_PATH):
    df = load_overrides(path)
    matches = df[
        (df['root'].str.lower() == root.lower()) &
        (df['register'].str.lower() == register.lower())
    ]
    if matches.empty:
        return None
    row = matches.iloc[0]
    return {
        'override': row['override'],
        'reason': row['reason'],
    }


def save_override(root: str, register: str, override: str, reason: str, path: Path = OVERRIDE_PATH) -> None:
    assert root.strip(), 'Override root must not be empty'
    assert register.strip(), 'Override register must not be empty'
    assert override.strip(), 'Override form must not be empty'
    assert reason.strip(), 'Override reason must not be empty'

    df = load_overrides(path)
    mask = (
        (df['root'].str.lower() == root.lower()) &
        (df['register'].str.lower() == register.lower())
    )
    df = df[~mask]
    new_row = {
        'root': root,
        'register': register,
        'override': override,
        'reason': reason,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df[OVERRIDE_COLUMNS].to_csv(path, index=False)
