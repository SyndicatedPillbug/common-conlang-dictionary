import streamlit as st
from pathlib import Path
import pandas as pd

from kharvunic.overrides import load_overrides

OVERRIDE_PATH = Path('data/overrides.csv')


def render():
    st.header('Override Manager')
    st.caption('Manage liturgical restorations, fossil forms, and prestige irregulars.')

    df = load_overrides()

    edited = st.data_editor(
        df,
        use_container_width=True,
        num_rows='dynamic',
    )

    if st.button('Save Overrides'):
        edited.to_csv(OVERRIDE_PATH, index=False)
        st.success('Overrides saved.')

    st.warning('Every override should include a historical or poetic reason.')
