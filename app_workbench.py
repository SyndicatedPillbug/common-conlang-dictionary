import streamlit as st

from kharvunic.ui import dictionary_page
from kharvunic.ui import evolution_page
from kharvunic.ui import export_page
from kharvunic.ui import history_page
from kharvunic.ui import overrides_page
from kharvunic.ui import phrase_page
from kharvunic.ui import rules_page
from kharvunic.ui import source_validation_page

st.set_page_config(page_title='Kharvunic Workbench', layout='wide')

st.title('Kharvunic Workbench')
st.caption('Diachronic dictionary, lineage tracer, and register workbench.')

PAGES = {
    'Evolution': evolution_page.render,
    'Dictionary': dictionary_page.render,
    'Phrase Builder': phrase_page.render,
    'Rules': rules_page.render,
    'Overrides': overrides_page.render,
    'History': history_page.render,
    'Source Validation': source_validation_page.render,
    'Exports': export_page.render,
}

page_name = st.sidebar.selectbox('Workbench Area', list(PAGES.keys()))

PAGES[page_name]()
