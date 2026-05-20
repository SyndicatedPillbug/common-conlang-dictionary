from pathlib import Path
import pandas as pd

DOMAIN_PATH = Path('data/semantic_domains.csv')


def load_domains(path: Path = DOMAIN_PATH):
    return pd.read_csv(path).fillna('')


def suggest_domains(meaning: str):
    meaning = meaning.lower()

    mapping = {
        'contract': 'law',
        'debt': 'trade',
        'prayer': 'temple',
        'ship': 'navigation',
        'fear': 'emotion',
        'star': 'cosmology',
        'fleet': 'military',
        'tax': 'administration',
        'hymn': 'poetry',
    }

    matches = []

    for key, domain in mapping.items():
        if key in meaning:
            matches.append(domain)

    return sorted(set(matches))
