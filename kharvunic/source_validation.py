from pathlib import Path
import pandas as pd

ALLOWED_SOURCE_LANGUAGES = {
    'Latin',
    'Vulgar Latin',
    'Old French',
    'French',
    'Italian',
    'Spanish',
    'Portuguese',
    'Romanian',
    'Occitan',
    'Catalan',
    'Romance Reconstruction',
}

ROOT_COLUMNS = ['root', 'meaning', 'source_language', 'notes']
ROOT_PATH = Path('data/roots.csv')


def load_roots(path: Path = ROOT_PATH) -> pd.DataFrame:
    df = pd.read_csv(path).fillna('')
    missing = set(ROOT_COLUMNS) - set(df.columns)
    assert not missing, f'Root file missing columns: {sorted(missing)}'
    return df[ROOT_COLUMNS]


def validate_root_row(row) -> list[str]:
    errors = []
    if not str(row.get('root', '')).strip():
        errors.append('missing root')
    if not str(row.get('meaning', '')).strip():
        errors.append('missing meaning')
    source = str(row.get('source_language', '')).strip()
    if not source:
        errors.append('missing source_language')
    elif source not in ALLOWED_SOURCE_LANGUAGES:
        errors.append(f'unrecognized source_language: {source}')
    return errors


def validate_roots(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for idx, row in df.iterrows():
        errors = validate_root_row(row)
        if errors:
            rows.append({
                'row': idx,
                'root': row.get('root', ''),
                'errors': '; '.join(errors),
            })
    return pd.DataFrame(rows)
