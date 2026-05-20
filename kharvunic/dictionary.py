import pandas as pd
from pathlib import Path

DICT_PATH = Path('data/dictionary.csv')


def load_dictionary():
    return pd.read_csv(DICT_PATH)


def save_entry(word, ipa, register, meaning, source_root, notes=''):
    df = load_dictionary()

    exists = (
        (df['word'] == word) &
        (df['register'] == register)
    ).any()

    if not exists:
        new_row = {
            'word': word,
            'ipa': ipa,
            'register': register,
            'meaning': meaning,
            'source_root': source_root,
            'notes': notes,
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DICT_PATH, index=False)


def fuzzy_search(df, query):
    q = query.lower()
    return df[
        df['word'].str.lower().str.contains(q) |
        df['meaning'].str.lower().str.contains(q) |
        df['source_root'].str.lower().str.contains(q)
    ]
