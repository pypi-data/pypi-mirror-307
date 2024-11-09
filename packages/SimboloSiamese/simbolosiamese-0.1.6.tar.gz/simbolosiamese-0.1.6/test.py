import re
import streamlit as st
from Siamese import BurmeseConverter

converter = BurmeseConverter()

tab1, tab2 = st.tabs(["Romanization to Burmese", "Burmese to Romanization"])

with tab1:
    text_input = st.text_input("Romanization to Burmese")
    st.write("Burmese output:", converter.romanization_to_burmese(text_input))

with tab2:
    text_input = st.text_input("Burmese to Romanization")
    st.write("Romanization output:", converter.burmese_to_romanization(text_input))