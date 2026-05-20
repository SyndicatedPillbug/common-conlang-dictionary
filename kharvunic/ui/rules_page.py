import streamlit as st
import pandas as pd
from pathlib import Path

from kharvunic.rule_library import RULE_COLUMNS, save_rules

RULE_PATH = Path('data/rules.csv')


def render():
    st.header('Rule Library')
    st.caption('View, edit, enable, disable, and reorder sound-change rules.')

    df = pd.read_csv(RULE_PATH).fillna('')

    edited = st.data_editor(
        df,
        use_container_width=True,
        num_rows='dynamic',
        column_order=RULE_COLUMNS,
    )

    if st.button('Save Rules'):
        save_rules(RULE_PATH, edited)
        st.success('Rules saved.')

    st.warning('Rule order matters. Save only after reviewing stage/register/order fields.')
