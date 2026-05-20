from pathlib import Path
import pandas as pd

from kharvunic.evolution import EvolutionEngine
from kharvunic.ipa import to_ipa
from kharvunic.overrides import find_override
from kharvunic.history import append_history
from kharvunic.domains import suggest_domains

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


def load_dictionary_v1(path: Path = DICT_PATH):
    df = pd.read_csv(path).fillna('')
    for col in DICT_COLUMNS:
        if col not in df.columns:
            df[col] = ''
    return df[DICT_COLUMNS]


def evolve_with_overrides(source: str, register: str):
    engine = EvolutionEngine()
    result = engine.evolve(source, register)

    override = find_override(source, register)
    if override:
        result_dict = {
            'source': result.source,
            'register': result.register,
            'result': override['override'],
            'ipa': to_ipa(override['override']),
            'trace': result.trace,
            'override_applied': True,
            'override_reason': override['reason'],
        }
    else:
        result_dict = {
            'source': result.source,
            'register': result.register,
            'result': result.result,
            'ipa': result.ipa,
            'trace': result.trace,
            'override_applied': False,
            'override_reason': '',
        }

    return result_dict


def save_word_entry(word, ipa, register, meaning, source_root, domain='', notes=''):
    assert word.strip(), 'word is required'
    assert register.strip(), 'register is required'
    assert meaning.strip(), 'meaning is required'
    assert source_root.strip(), 'source_root is required'

    df = load_dictionary_v1()

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
    df[DICT_COLUMNS].sort_values('word').to_csv(DICT_PATH, index=False)

    append_history(
        word=word,
        register=register,
        previous_form=previous,
        new_form=str(row),
        reason='saved through v1 workflow',
    )

    return row
