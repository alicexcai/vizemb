from re import S
import streamlit as st
from modules.VizEmb import *
import plotly.express as px
import pandas as pd
from modules import embed
from sklearn.neighbors import NearestNeighbors

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
    # properties = list(thisVizEmbData.properties["sem"]) + list(thisVizEmbData.properties["cat"]) + list(thisVizEmbData.properties["quant"])
    quant_properties = list(thisVizEmbData.properties["quant"])
    cat_properties = list(thisVizEmbData.properties["cat"])

    # @st.cache
    # def generate_default_embeddings():
    #     with st.spinner("Calculating embeddings..."):
    #         thisVizEmbData.compose_default_embedding()
    #         thisVizEmbData.reduce2oned_embedding_df()
    #         st.success("Embeddings generated.")
    
    st.markdown("""
    ### Compare Two Items
    """)

    # @st.cache
    # def generate_default_embeddings():
    #     with st.spinner("Calculating embeddings..."):
    #         thisVizEmbData.compose_default_embedding()
    #         thisVizEmbData.reduce2oned_embedding_df()
    #         st.success("Embeddings generated.")

    # # initialize session state for generated to false
    # if 'generated' not in st.session_state:
    #     st.session_state.generated = False

    # if st.button("Generate embeddings for comparison"):
    #     generate_default_embeddings()
    #     st.session_state.generated = True

    # search_params.item_names = st.selectbox("Select item names", thisVizEmbData.colvalue_df["TITLE"])


    def calculate_similarity(value1, value2, property):
        range = thisVizEmbData.properties["quant"][property]["max"] - thisVizEmbData.properties["quant"][property]["min"]
        return (value1 - value2) / range

    def calculate_percentile(value, property):
        range = thisVizEmbData.properties["quant"][property]["max"] - thisVizEmbData.properties["quant"][property]["min"]
        scaled = (value - thisVizEmbData.properties["quant"][property]["min"]) / range
        return scaled


    col1, col2 = st.columns(2)
    item1 = col1.selectbox("Select first item", item_dict.keys())
    item2 = col2.selectbox("Select second item", item_dict.keys())


    def generate_comparison(item1, item2):
        index1 = item_dict[item1]
        index2 = item_dict[item2]

        col1, col2 = st.columns(2)
        with col1.expander(f"{item1} data"):
            st.write(thisVizEmbData.df[thisVizEmbData.df["[title] TITLE"] == item1])
            datadict1 = thisVizEmbData.df[thisVizEmbData.df["[title] TITLE"] == item1].to_dict()
            datadict1.pop("Unnamed: 0")
            st.write({key: list(value.values())[0] for key, value in datadict1.items()})
        with col2.expander(f"{item2} data"):
            st.write(thisVizEmbData.df[thisVizEmbData.df["[title] TITLE"] == item2])
            datadict2 = thisVizEmbData.df[thisVizEmbData.df["[title] TITLE"] == item2].to_dict()
            datadict2.pop("Unnamed: 0")
            st.write({key: list(value.values())[0] for key, value in datadict2.items()})
            
        percentile_df1 = [calculate_percentile(thisVizEmbData.df[prop][index1], prop) for prop in quant_properties]
        percentile_df2 = [calculate_percentile(thisVizEmbData.df[prop][index2], prop) for prop in quant_properties]
        value_df1 = [thisVizEmbData.df[prop][index1] for prop in quant_properties]
        value_df2=[thisVizEmbData.df[prop][index2] for prop in quant_properties]
        # similarity plotly graph 
        item1_quant_dict = dict(percentile=percentile_df1, value=value_df1, stage=quant_properties)
        item2_quant_dict = dict(percentile=percentile_df2, value=value_df2, stage=quant_properties)

        df1 = pd.DataFrame(item1_quant_dict)
        df1['title'] = item1
        df2 = pd.DataFrame(item2_quant_dict)
        df2['title'] = item2
        df = pd.concat([df1, df2], axis=0)
        fig = px.funnel(df, x='percentile', y='stage', color='title', hover_data=['value'], title=f"{item1} vs {item2}")
        st.write(fig)

    generate_comparison(item1, item2)

    def find_similar_items(item1, num_similar_items):
        embed.generate_default_embeddings(thisVizEmbData) # if st.session_state.generated == False else None
        embeddings = np.array(thisVizEmbData.default_embedding_df.unraveled)
        knn = NearestNeighbors(n_neighbors=num_similar_items)
        knn.fit(embeddings)
        index = item_dict[item1]
        similar_items = knn.kneighbors([embeddings[index]], return_distance=False)
        # print(type(similar_items))
        return similar_items.tolist()[0]

    st.markdown("""
    ---
    ### Find Similar Items
    """)
    selected_item = st.selectbox("Select item", item_dict.keys())
    num_similar_items = st.slider("Number of similar items", 1, 10, 1)
    # index1 = item_dict[selected_item]
    with st.expander("Item data"):
        st.write(thisVizEmbData.df[thisVizEmbData.df["[title] TITLE"] == selected_item])

    if st.button("Find similar items"):
        results = find_similar_items(selected_item, num_similar_items+1)
        # st.write(results)
        for result in results:
            item = thisVizEmbData.df["[title] TITLE"][result]
            generate_comparison(selected_item, item)