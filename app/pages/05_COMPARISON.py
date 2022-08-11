import streamlit as st
from modules.VizEmb import *
import plotly.express as px
import pandas as pd
from modules import embed
from sklearn.neighbors import NearestNeighbors

st.markdown("""
# COMPARISON
*Compare and find similar items in your database.*
""")

if thisVizEmbData.df is None:
    st.success("No data loaded. Please load your database in START.")
else:

    # calculate fundamentals

    parameter_list = thisVizEmbData.df.columns.tolist()
    thisVizEmbData.get_colvalues("title")
    thisVizEmbData.parse_cat_dfs()
    item_dict = {value: i for i, value in enumerate(thisVizEmbData.colvalue_df["title"]["[title] TITLE"].tolist())}
    quant_properties = list(thisVizEmbData.properties["quant"])
    cat_properties = list(thisVizEmbData.properties["cat"])

    # calculate percentile of property values

    def calculate_percentile(value, property):
        range = thisVizEmbData.properties["quant"][property]["max"] - thisVizEmbData.properties["quant"][property]["min"]
        scaled = (value - thisVizEmbData.properties["quant"][property]["min"]) / range
        return scaled

    # compare two items
    
    st.markdown("""
    ### Compare Two Items
    """)

    col1, col2 = st.columns(2)
    item1 = col1.selectbox("Select first item", item_dict.keys())
    item2 = col2.selectbox("Select second item", item_dict.keys())

    # generate comparison

    def generate_comparison(item1, item2):
        index1 = item_dict[item1]
        index2 = item_dict[item2]

        col1, col2 = st.columns(2)
        with col1.expander(f"{item1} data"):
            st.write(thisVizEmbData.df[thisVizEmbData.df["[title] TITLE"] == item1])
            datadict1 = thisVizEmbData.df[thisVizEmbData.df["[title] TITLE"] == item1].to_dict()
            st.write({key: list(value.values())[0] for key, value in datadict1.items()})
            img1path = thisVizEmbData.df.filter(regex="img").iloc[index1].values[0]
            st.image(img1path)
        with col2.expander(f"{item2} data"):
            st.write(thisVizEmbData.df[thisVizEmbData.df["[title] TITLE"] == item2])
            datadict2 = thisVizEmbData.df[thisVizEmbData.df["[title] TITLE"] == item2].to_dict()
            st.write({key: list(value.values())[0] for key, value in datadict2.items()})
            img2path = thisVizEmbData.df.filter(regex="img").iloc[index1].values[0]
            st.image(img2path)
            
        percentile_df1 = [calculate_percentile(thisVizEmbData.df[prop][index1], prop) for prop in quant_properties]
        percentile_df2 = [calculate_percentile(thisVizEmbData.df[prop][index2], prop) for prop in quant_properties]
        value_df1 = [thisVizEmbData.df[prop][index1] for prop in quant_properties]
        value_df2=[thisVizEmbData.df[prop][index2] for prop in quant_properties]
        item1_quant_dict = dict(percentile=percentile_df1, value=value_df1, stage=quant_properties)
        item2_quant_dict = dict(percentile=percentile_df2, value=value_df2, stage=quant_properties)
        
        df1 = pd.DataFrame(item1_quant_dict)
        df1['title'] = item1
        df2 = pd.DataFrame(item2_quant_dict)
        df2['title'] = item2

        # display graph

        df = pd.concat([df1, df2], axis=0)
        fig = px.funnel(df, x='percentile', y='stage', color='title', hover_data=['value'], title=f"{item1} vs {item2}")
        st.write(fig)

    generate_comparison(item1, item2)

    # find nearest neighbors

    def find_similar_items(item1, num_similar_items):
        embed.generate_default_embeddings(thisVizEmbData) # if st.session_state.generated == False else None
        embeddings = np.array(thisVizEmbData.default_embedding_df.unraveled)
        knn = NearestNeighbors(n_neighbors=num_similar_items)
        knn.fit(embeddings)
        index = item_dict[item1]
        similar_items = knn.kneighbors([embeddings[index]], return_distance=False)
        return similar_items.tolist()[0]

    st.markdown("""
    ---
    ### Find Similar Items
    """)

    selected_item = st.selectbox("Select item", item_dict.keys())
    num_similar_items = st.slider("Number of similar items", 1, 10, 1)

    with st.expander("Item data"):
        index = item_dict[selected_item]
        st.write(thisVizEmbData.df[thisVizEmbData.df["[title] TITLE"] == selected_item])
        datadict = thisVizEmbData.df[thisVizEmbData.df["[title] TITLE"] == selected_item].to_dict()
        st.write({key: list(value.values())[0] for key, value in datadict.items()})
        imgpath = thisVizEmbData.df.filter(regex="img").iloc[index].values[0]
        st.image(imgpath)

    if st.button("Find similar items"):
        results = find_similar_items(selected_item, num_similar_items+1)
        for result in results:
            item = thisVizEmbData.df["[title] TITLE"][result]
            generate_comparison(selected_item, item)