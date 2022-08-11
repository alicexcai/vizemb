import streamlit as st
from modules.VizEmb import *
from modules import embed, neurafutures

st.markdown("""
## GETTING STARTED
Load your database to get started. Make sure your database follows the specified schema. Label your columns with the correct types.
""")

# load database

# thisVizEmbData.project_name = st.text_input("Enter your project name:", thisVizEmbData.project_name)
uploaded_file = st.file_uploader("Upload database", type = ['csv']) # , 'xlsx', 'sqlite', 'db'])

if uploaded_file:
    thisVizEmbData.save_db_file(uploaded_file)
    
    thisVizEmbData.load_df()
    st.success("Your database has been loaded.")

    # preprocess database

    # special preprocessing for NEURAFUTURES
    thisVizEmbData.df = neurafutures.neurafuture_preprocessing(thisVizEmbData.unprocessed_df)
    st.success("Your database has been preprocessed.")

    st.markdown("---")

    # show database details

    if thisVizEmbData.df is not None:
        
        thisVizEmbData.get_properties()
        thisVizEmbData.split_df()
        thisVizEmbData.parse_cat_dfs()

        with st.expander("View quantitative data"):
            st.markdown("""### Quantitative data""")
            st.write(thisVizEmbData.properties["quant"])
            st.write(thisVizEmbData.quant_df)
        with st.expander("View categorical data"):
            st.markdown("""### Categorical data""")
            st.write(thisVizEmbData.properties["cat"])
            st.write(thisVizEmbData.cat_df)
        with st.expander("View semantic data"):
            st.markdown("""### View semantic data""")
            st.write(thisVizEmbData.properties["sem"])
            st.write(thisVizEmbData.sem_df)
        with st.expander("View full database"):
            st.markdown("""### Full database""")
            st.write(thisVizEmbData.df)

