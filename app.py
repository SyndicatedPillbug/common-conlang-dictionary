import streamlit as st
from kharvunic.engine import Evolver

st.title('Kharvunic Evolution Engine')

word = st.text_input('Source Romance/Latin Root', 'misericordia')
register = st.selectbox('Target Register', ['common', 'temple', 'boardroom', 'trade'])

if st.button('Evolve'):
    e = Evolver()
    result = e.evolve(word, register)

    st.subheader('Result')
    st.write(result['result'])

    st.subheader('Trace')
    for step in result['trace']:
        st.write(step)
