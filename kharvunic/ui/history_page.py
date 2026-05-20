import streamlit as st

from kharvunic.history import load_history


def render():
    st.header('Dictionary History')
    st.caption('Inspect lexical changes over time.')

    history = load_history()

    search = st.text_input('Search History')

    if search:
        mask = (
            history['word'].str.contains(search, case=False, na=False) |
            history['reason'].str.contains(search, case=False, na=False)
        )
        history = history[mask]

    st.dataframe(history, use_container_width=True)
