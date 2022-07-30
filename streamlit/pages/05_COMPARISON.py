import streamlit as st
from modules.VizEmb import *
import plotly.express as px
import pandas as pd

st.markdown("""
# COMPARISON
*compare items in your database*
""")

if thisVizEmbData.df is None:
    st.success("No data loaded. Please load your database in START.")
else:

    parameter_list = thisVizEmbData.df.columns.tolist()
    thisVizEmbData.get_colvalues("title")
    thisVizEmbData.parse_cat_dfs()
    item_dict = {value: i for i, value in enumerate(thisVizEmbData.colvalue_df["title"]["[title] TITLE"].tolist())}
    properties = list(thisVizEmbData.properties["sem"]) + list(thisVizEmbData.properties["cat"]) + list(thisVizEmbData.properties["quant"])

    @st.cache
    def generate_default_embeddings():
        with st.spinner("Calculating embeddings..."):
            thisVizEmbData.compose_default_embedding()
            thisVizEmbData.reduce2oned_embedding_df()
            st.success("Embeddings generated.")

    # initialize session state for generated to false
    if 'generated' not in st.session_state:
        st.session_state.generated = False

    if st.button("Generate embeddings for comparison"):
        generate_default_embeddings()
        st.session_state.generated = True

    # search_params.item_names = st.selectbox("Select item names", thisVizEmbData.colvalue_df["TITLE"])
    item1 = st.selectbox("Select first item", item_dict.keys())
    index1 = item_dict[item1]
    item2 = st.selectbox("Select second item", item_dict.keys())
    index2 = item_dict[item2]

    with st.expander("See raw data"):
        st.write(thisVizEmbData.df)
    # selected_ranker = st.selectbox("Select ranker", properties)

    if st.session_state.generated == True:

        # similarity plotly graph 
        item1_dict = dict(value=[thisVizEmbData.oned_embedding_df[prop][index1] for prop in properties], stage=properties)
        item2_dict = dict(value=[thisVizEmbData.oned_embedding_df[prop][index2] for prop in properties], stage=properties)

        df1 = pd.DataFrame(item1_dict)
        df1['title'] = item1
        df2 = pd.DataFrame(item2_dict)
        df2['title'] = item2
        df = pd.concat([df1, df2], axis=0)
        fig = px.funnel(df, x='value', y='stage', color='title')
        st.write(fig)
