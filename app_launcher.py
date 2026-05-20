import streamlit as st

from kharvunic.ui import evolution_page
from kharvunic.ui import phrase_page
from kharvunic.ui import dictionary_page

st.set_page_config(page_title='Kharvunic Workbench', layout='wide')

st.title('Kharvunic Workbench')

mode = st.sidebar.selectbox(
    'Workbench Area',
    [
        'Evolution',
        'Phrase Builder',
        'Dictionary',
    ]
)

if mode == 'Evolution':
    evolution_page.render()
elif mode == 'Phrase Builder':
    phrase_page.render()
elif mode == 'Dictionary':
    dictionary_page.render()
