from pathlib import Path
import pandas as pd

DOMAIN_PATH = Path('data/semantic_domains.csv')


def load_domains(path: Path = DOMAIN_PATH):
    return pd.read_csv(path).fillna('')


def suggest_domains(meaning: str):
    meaning = meaning.lower()

    mapping = {
        'contract': 'law',
        'obligation': 'law',
        'debt': 'trade',
        'market': 'trade',
        'prayer': 'temple',
        'sacred': 'temple',
        'ship': 'navigation',
        'walk': 'body',
        'movement': 'body',
        'tear': 'emotion',
        'weep': 'emotion',
        'mercy': 'emotion',
        'fear': 'emotion',
        'star': 'cosmology',
        'heaven': 'cosmology',
        'fleet': 'military',
        'guard': 'military',
        'tax': 'administration',
        'answer': 'administration',
        'hymn': 'poetry',
    }

    matches = []

    for key, domain in mapping.items():
        if key in meaning:
            matches.append(domain)

    return sorted(set(matches))
