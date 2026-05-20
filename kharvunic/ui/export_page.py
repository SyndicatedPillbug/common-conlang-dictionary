import streamlit as st
from pathlib import Path

from kharvunic.dictionary import load_dictionary
from kharvunic.export_csv import export_csv
from kharvunic.export_json import export_json
from kharvunic.export_markdown import export_markdown
from kharvunic.export_anki import export_anki

EXPORT_DIR = Path('exports')


def render():
    st.header('Exports')

    dictionary = load_dictionary()

    if st.button('Export CSV'):
        path = EXPORT_DIR / 'dictionary.csv'
        export_csv(dictionary, path)
        st.success(f'Exported {path}')

    if st.button('Export JSON'):
        path = EXPORT_DIR / 'dictionary.json'
        export_json(dictionary, path)
        st.success(f'Exported {path}')

    if st.button('Export Markdown'):
        path = EXPORT_DIR / 'dictionary.md'
        export_markdown(dictionary, path)
        st.success(f'Exported {path}')

    if st.button('Export Anki TSV'):
        path = EXPORT_DIR / 'dictionary_anki.tsv'
        export_anki(dictionary, path)
        st.success(f'Exported {path}')
