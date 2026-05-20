import streamlit as st

from kharvunic.workflows import evolve_with_overrides
from kharvunic.workflows import save_word_entry
from kharvunic.dictionary import load_dictionary
from kharvunic.collision import find_collisions
from kharvunic.domains import suggest_domains


def render():
    st.header('Evolution Workbench')

    source = st.text_input('Source Romance/Latin Root', 'misericordia')

    meaning = st.text_input('Meaning', 'mercy')

    register = st.selectbox(
        'Target Register',
        ['temple', 'boardroom', 'trade']
    )

    if st.button('Evolve'):
        result = evolve_with_overrides(source, register)

        st.subheader('Result')
        st.write(result['result'])

        st.subheader('IPA')
        st.write(result['ipa'])

        if result['override_applied']:
            st.subheader('Override Applied')
            st.info(result['override_reason'])

        st.subheader('Lineage Trace')
        for step in result['trace']:
            st.write(f"[{step.stage}] {step.form}")
            if step.note:
                st.caption(step.note)

        dictionary = load_dictionary().to_dict(orient='records')
        collisions = find_collisions(dictionary, result['result'])

        if collisions:
            st.subheader('Potential Collisions')
            st.json(collisions)

        suggested = suggest_domains(meaning)

        domain = st.selectbox(
            'Semantic Domain',
            suggested if suggested else [''],
        )

        notes = st.text_area('Notes')

        if st.button('Save Word'):
            save_word_entry(
                word=result['result'],
                ipa=result['ipa'],
                register=register,
                meaning=meaning,
                source_root=source,
                domain=domain,
                notes=notes,
            )
            st.success('Word saved to dictionary.')
