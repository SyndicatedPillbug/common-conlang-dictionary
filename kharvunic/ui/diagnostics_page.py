import streamlit as st

from kharvunic.diagnostic_runner import run_diagnostics


def render():
    st.header('Diagnostics')
    st.caption('Probe whether the evolution engine is doing real linguistic work.')

    if st.button('Run Diagnostic Corpus'):
        results = run_diagnostics()
        st.dataframe(results, use_container_width=True)

        warnings = results[results['warnings'] != '']
        if not warnings.empty:
            st.subheader('Warnings')
            st.dataframe(warnings, use_container_width=True)
