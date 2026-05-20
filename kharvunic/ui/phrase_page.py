import streamlit as st

from kharvunic.dictionary import load_dictionary
from kharvunic.phrase_builder import analyze_phrase


def render():
    st.header('Phrase Builder')

    text = st.text_area(
        'Phrase',
        'Rhesht plorēsh lakrem vel lath'
    )

    if st.button('Analyze Phrase'):
        dictionary = load_dictionary()
        known = set(dictionary['word'].str.lower())

        result = analyze_phrase(text, known)

        st.subheader('IPA')
        st.write(result['ipa'])

        st.subheader('Rhythm')
        st.json({
            'syllables': result['syllables'],
            'stress': result['stress'],
            'cadence': result['cadence'],
        })

        if result['unknown_words']:
            st.subheader('Unknown Words')
            st.write(result['unknown_words'])
