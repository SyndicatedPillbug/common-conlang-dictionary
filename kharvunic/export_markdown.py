from pathlib import Path
import pandas as pd


def export_markdown(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = ['# Kharvunic Dictionary', '']

    for _, row in df.sort_values('word').iterrows():
        lines.append(f"## {row['word']}")
        lines.append(f"- IPA: `{row['ipa']}`")
        lines.append(f"- Register: {row['register']}")
        lines.append(f"- Meaning: {row['meaning']}")
        lines.append(f"- Source Root: {row['source_root']}")

        notes = str(row.get('notes', '')).strip()
        if notes:
            lines.append(f"- Notes: {notes}")

        lines.append('')

    path.write_text('\n'.join(lines), encoding='utf-8')
