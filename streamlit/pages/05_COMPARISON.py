import streamlit as st
from modules.VizEmb import *

st.markdown("""
# COMPARISON
*compare items in your database*
""")

if not thisVizEmbData.df:
    st.success("No data loaded. Please load your database in START.")
else:
    with st.expander("See raw data"):
        st.write(thisVizEmbData.df)
    parameter_list = thisVizEmbData.df.columns.tolist()