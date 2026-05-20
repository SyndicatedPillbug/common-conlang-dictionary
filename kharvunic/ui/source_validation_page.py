import streamlit as st

from kharvunic.source_validation import load_roots, validate_roots


def render():
    st.header('Source Validation')
    st.caption('Ensure all roots retain real etymological ancestry.')

    roots = load_roots()
    issues = validate_roots(roots)

    if issues.empty:
        st.success('No source validation issues found.')
    else:
        st.warning('Validation issues detected.')
        st.dataframe(issues, use_container_width=True)
