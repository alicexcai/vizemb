import streamlit as st


t = st.radio("Toggle to see font change", [True, False])

if t:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&family=Space+Grotesk:wght@300&family=Space+Mono&display=swap');
    html, body, [class*="css"]  {
    font-family: 'Roboto', sans-serif;
    font-family: 'Space Grotesk', sans-serif;
    font-family: 'Space Mono', monospace;
    }
    </style>
    """, unsafe_allow_html=True)

"# Hello"

"""This font will look different, based on your choice of radio button"""