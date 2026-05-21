from pathlib import Path
import pandas as pd

from kharvunic.domains import suggest_domains
from kharvunic.evolution_v2 import EvolutionEngineV2
from kharvunic.history import HISTORY_PATH, append_history

DICT_PATH = Path('data/dictionary.csv')
DICT_COLUMNS = [
    'word',
    'ipa',
    'register',
    'meaning',
    'source_root',
    'domain',
    'notes',
]
SAVEABLE_HEALTH = {'passing'}


def load_dictionary_v1(path: Path = DICT_PATH):
    df = pd.read_csv(path).fillna('')
    for col in DICT_COLUMNS:
        if col not in df.columns:
            df[col] = ''
    return df[DICT_COLUMNS]


def load_dictionary_v2(path: Path = DICT_PATH):
    return load_dictionary_v1(path)


def evolve_with_overrides(source: str, register: str):
    """Backward-compatible workflow wrapper now powered by EvolutionEngineV2."""
    engine = EvolutionEngineV2()
    return engine.evolve(source, register)


def find_existing_entry(word: str, register: str, path: Path = DICT_PATH) -> list[dict]:
    df = load_dictionary_v1(path)
    mask = (
        (df['word'].str.lower() == word.lower()) &
        (df['register'].str.lower() == register.lower())
    )
    return df[mask].to_dict(orient='records')


def save_blocker_reason(result: dict) -> str:
    """Return an empty string when a v2 evolution result is canonical-saveable.

    Weak and failing candidates are useful diagnostics, but they should not enter
    the canonical dictionary by accident. The app can still show their lineage;
    saving requires fixing the rule set or adding a deliberate override first.
    """
    diagnostics = result.get('diagnostics', {})
    health = diagnostics.get('health', 'weak')
    warnings = diagnostics.get('warnings', [])

    if health not in SAVEABLE_HEALTH:
        detail = '; '.join(warnings) if warnings else f'health={health}'
        return (
            'candidate health is not passing. Fix the rule set or add an explicit '
            f'override before saving. Details: {detail}'
        )

    if warnings:
        return 'candidate has unresolved diagnostics: ' + '; '.join(warnings)

    return ''


def is_saveable_result(result: dict) -> bool:
    return save_blocker_reason(result) == ''


def save_word_entry(
    word,
    ipa,
    register,
    meaning,
    source_root,
    domain='',
    notes='',
    path: Path = DICT_PATH,
    history_path: Path = HISTORY_PATH,
    reason='saved through v2 workflow',
):
    assert word.strip(), 'word is required'
    assert ipa.strip(), 'ipa is required'
    assert register.strip(), 'register is required'
    assert meaning.strip(), 'meaning is required'
    assert source_root.strip(), 'source_root is required'

    df = load_dictionary_v1(path)

    mask = (
        (df['word'].str.lower() == word.lower()) &
        (df['register'].str.lower() == register.lower())
    )

    previous = ''
    if mask.any():
        previous = str(df.loc[mask].iloc[0].to_dict())
        df = df[~mask]

    if not domain:
        suggestions = suggest_domains(meaning)
        domain = suggestions[0] if suggestions else ''

    assert domain.strip(), 'domain is required'

    row = {
        'word': word,
        'ipa': ipa,
        'register': register,
        'meaning': meaning,
        'source_root': source_root,
        'domain': domain,
        'notes': notes,
    }

    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df[DICT_COLUMNS].sort_values(['register', 'word']).to_csv(path, index=False)

    append_history(
        word=word,
        register=register,
        previous_form=previous,
        new_form=str(row),
        reason=reason,
        path=history_path,
    )

    return row


def save_evolution_result(
    result: dict,
    meaning: str,
    domain: str,
    notes: str = '',
    path: Path = DICT_PATH,
    history_path: Path = HISTORY_PATH,
    reason: str = 'saved through v2 workbench',
):
    blocker = save_blocker_reason(result)
    if blocker:
        raise ValueError('Cannot save v2 result: ' + blocker)

    return save_word_entry(
        word=result['result'],
        ipa=result['ipa'],
        register=result['register'],
        meaning=meaning,
        source_root=result['source'],
        domain=domain,
        notes=notes,
        path=path,
        history_path=history_path,
        reason=reason,
    )
