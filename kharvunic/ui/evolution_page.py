import streamlit as st

from kharvunic.evolution import EvolutionEngine
from kharvunic.dictionary import load_dictionary
from kharvunic.collision import find_collisions


def render():
    st.header('Evolution')

    engine = EvolutionEngine()

    source = st.text_input('Source Root', 'misericordia')

    register = st.selectbox(
        'Register',
        ['temple', 'boardroom', 'trade']
    )

    if st.button('Evolve Word'):
        result = engine.evolve(source, register)

        st.subheader('Result')
        st.write(result.result)

        st.subheader('IPA')
        st.write(result.ipa)

        st.subheader('Lineage Trace')
        for step in result.trace:
            st.write(f"[{step.stage}] {step.form}")
            if step.note:
                st.caption(step.note)

        dictionary = load_dictionary().to_dict(orient='records')
        collisions = find_collisions(dictionary, result.result)

        if collisions:
            st.subheader('Potential Collisions')
            st.json(collisions)
