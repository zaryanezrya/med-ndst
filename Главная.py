import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Главная")

st.markdown(
    """
    Приложение разработано с использованием skelarn, pandas и streamlit 

    ## Возможности:
    1. Анализ вероятности развития ЖЭС
    2. ...
"""
)