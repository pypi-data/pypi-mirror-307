import streamlit as st
from st_default_width import (
    set_use_container_width_default,
    revert_use_container_width_default,
)

if st.toggle("Make `use_container_width = True`"):
    set_use_container_width_default()
else:
    revert_use_container_width_default()

st.divider()
with st.echo():
    st.image("https://placehold.co/100x50")
    st.button("Botón")
