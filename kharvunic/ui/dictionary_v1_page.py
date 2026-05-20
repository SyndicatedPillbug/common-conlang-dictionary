import streamlit as st

from kharvunic.workflows import load_dictionary_v1


def render():
    st.header('Dictionary')

    dictionary = load_dictionary_v1()

    search = st.text_input('Search')

    if search:
        mask = (
            dictionary['word'].str.contains(search, case=False, na=False) |
            dictionary['meaning'].str.contains(search, case=False, na=False) |
            dictionary['source_root'].str.contains(search, case=False, na=False) |
            dictionary['domain'].str.contains(search, case=False, na=False)
        )
        dictionary = dictionary[mask]

    sort_mode = st.selectbox('Sort', ['A-Z', 'Z-A'])
    ascending = sort_mode == 'A-Z'

    dictionary = dictionary.sort_values('word', ascending=ascending)

    st.dataframe(dictionary, use_container_width=True)
