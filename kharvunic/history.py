"""Dictionary history tracking.

No lexical form should silently mutate.
All changes become historically inspectable.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

HISTORY_COLUMNS = [
    'timestamp',
    'word',
    'register',
    'previous_form',
    'new_form',
    'reason',
]

HISTORY_PATH = Path('data/dictionary_history.csv')


def ensure_history_file(path: Path = HISTORY_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        pd.DataFrame(columns=HISTORY_COLUMNS).to_csv(path, index=False)


def append_history(word: str, register: str, previous_form: str, new_form: str, reason: str, path: Path = HISTORY_PATH) -> None:
    assert word.strip(), 'History word must not be empty'
    assert register.strip(), 'History register must not be empty'
    assert reason.strip(), 'History reason must not be empty'

    ensure_history_file(path)

    df = pd.read_csv(path).fillna('')

    row = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'word': word,
        'register': register,
        'previous_form': previous_form,
        'new_form': new_form,
        'reason': reason,
    }

    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df[HISTORY_COLUMNS].to_csv(path, index=False)


def load_history(path: Path = HISTORY_PATH):
    ensure_history_file(path)
    return pd.read_csv(path).fillna('')
