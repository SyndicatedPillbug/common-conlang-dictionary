import streamlit as st

from kharvunic.ui import evolution_v1_page
from kharvunic.ui import dictionary_v1_page
from kharvunic.ui import phrase_page
from kharvunic.ui import rules_page
from kharvunic.ui import overrides_page
from kharvunic.ui import history_page
from kharvunic.ui import source_validation_page
from kharvunic.ui import export_page

st.set_page_config(page_title='Kharvunic Workbench v1', layout='wide')

st.title('Kharvunic Workbench v1')
st.caption('Temple Common / Boardroom Common / Trade Common diachronic workbench')

PAGES = {
    'Evolution': evolution_v1_page.render,
    'Dictionary': dictionary_v1_page.render,
    'Phrase Builder': phrase_page.render,
    'Rules': rules_page.render,
    'Overrides': overrides_page.render,
    'History': history_page.render,
    'Source Validation': source_validation_page.render,
    'Exports': export_page.render,
}

page = st.sidebar.selectbox('Workbench Area', list(PAGES.keys()))

PAGES[page]()
