from pathlib import Path
import pandas as pd


def export_anki(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for _, row in df.iterrows():
        rows.append('\t'.join([
            str(row['word']),
            str(row['ipa']),
            str(row['meaning']),
            str(row['register']),
            str(row['source_root']),
        ]))

    path.write_text('\n'.join(rows), encoding='utf-8')
