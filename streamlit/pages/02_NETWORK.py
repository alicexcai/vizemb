import streamlit as st
from modules.VizEmb import *
import plotly.express as px
import tensorflow as tf

### CLASSES (move to separate file) ###
 
class Params:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class QuantParam:
    def __init__(self, name, min, max):
        self.name = name
        self.min = min
        self.max = max

class CatParam:
    def __init__(self, name, values):
        self.name = name
        self.values = values

search_params = Params(
    item_names = [],
    quant_params = [], # QuantParam(name, min, max)
    cat_params = [] # CatParam(name, values)
)

embedding_params = Params(
    property_weights = {},
    mode = None, # "global" or "local"
    color = None, # rainbow
    num_nodes = None
)

### PAGE SETUP ###

st.markdown("""
# NETWORK
*visualize your data in a shared embedding space*
""")

# @st.cache
# def filter_df():
#     thisVizEmbData.filter_df("TITLE")
# filter_df()
if thisVizEmbData.df is None:
    st.success("No data loaded. Please load your database in START.")
else:
    
    # FILTER DATA

    with st.sidebar:
        
        thisVizEmbData.filter_df("TITLE")
        thisVizEmbData.parse_cat_dfs()
        search_params.item_names = st.selectbox("Select item names", thisVizEmbData.filtered_df["TITLE"])
        search_params.search_keywords = st.text_input("Search keywords", "")
        
        st.write("### Filters")
        if st.button("Apply filters"):
            # thisVizEmbData.filter_df(search_params.item_names, search_params.search_keywords)
            # thisVizEmbData.parse_cat_dfs()
            st.success("Filters applied.")

        for quantprop in thisVizEmbData.properties["quant"]:
            quantprop_value = st.slider(quantprop, float(thisVizEmbData.properties["quant"][quantprop]["min"]), float(thisVizEmbData.properties["quant"][quantprop]["max"]), (float(thisVizEmbData.properties["quant"][quantprop]["min"]), float(thisVizEmbData.properties["quant"][quantprop]["max"])))
            search_params.quant_params.append(QuantParam(quantprop, quantprop_value[0], quantprop_value[1]))
            # search_params.quant_params.append(QuantParam(quantprop, quantprop_value, quantprop_value))

        for catprop in thisVizEmbData.properties["cat"]:
            catprop_value = st.selectbox(catprop, thisVizEmbData.cat_values[catprop])
            search_params.cat_params.append(CatParam(catprop, catprop_value))
        
        st.markdown("---")


        # st.sidebar.slider("Filter by", "TITLE", min_value=0, max_value=len(thisVizEmbData.filtered_df["TITLE"])-1, value=0)

    # EMBEDDING PARAMETERS

    with st.expander("Embedding Parameters"):
        for property in list(thisVizEmbData.properties["quant"].keys()) + list(thisVizEmbData.properties["cat"].keys()) + list(thisVizEmbData.properties["sem"].keys()):
            if st.checkbox(property, True):
                embedding_params.property_weights[property] = st.slider(property, 0, 1, 1)
    
    with st.expander("Visualization Paramters"):
        embedding_params.num_nodes = st.slider("# of Nodes", 1, thisVizEmbData.df.shape[0], 10)
        embedding_params.mode = st.selectbox("Mode", ["global", "local"])
        embedding_params.color = st.selectbox("Color", ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "black", "white"])
        embedding_params.graph_title = st.text_input("Enter your graph title", "")
        embedding_params.hover_data = st.multiselect("Select data to display on hover", thisVizEmbData.df.columns.tolist())

    with st.spinner("Calculating embeddings..."):

        # @st.cache
        def calculate_default_embeddings():
            thisVizEmbData.compose_default_embedding()
        calculate_default_embeddings()
        st.success("Embeddings calculated.")
    # thisVizEmbData.default_embedding_df.highdim = pd.read_pickle("/Users/alicecai/Desktop/vizemb/streamlit/default_embedding_df_highdim.pkl")

    # # GENERATE EMBEDDINGS
    # if st.button("GENERATE SPECIFIC EMBEDDINGS"):
    #     thisVizEmbData.compose_specified_embedding(embedding_params, search_params)

    # REDUCE EMBEDDING DIMENSIONALITY
    st.write(thisVizEmbData.default_embedding_df.highdim.drop("[gen] composite_embedding", axis=1))


    # thisVizEmbData.default_embedding_df.reduced = None # tf.keras.layers.GlobalAveragePooling1D()(thisVizEmbData.default_embedding_df)
    # # t-SNE dimensionality reduction
    # thisVizEmbData.default_embedding_df.twod = None 

    # if st.button("EXPAND EMBEDDINGS"):
    #     with st.spinner("Expanding embeddings..."):
    #         thisVizEmbData.expand_embedding(thisVizEmbData.default_embedding_df)
    #         st.write(thisVizEmbData.default_embedding_df.expanded.drop(columns=["[gen] expanded_composite_embedding", "[gen] composite_embedding"], axis=1))
    #         st.success("Embeddings expanded.")
    
    if st.button("REDUCE DIMENSIONALITY"):
        with st.spinner("Reducing dimensionality..."):
            thisVizEmbData.reduce2twod_embedding_df(thisVizEmbData.default_embedding_df)
            # st.write("reduced_embedding_df", thisVizEmbData.default_embedding_df.twod)
            st.success("Dimensionality reduced.")

    # VISUALIZE EMBEDDINGS
            # fig = plt.figure(figsize=(12, 12))
            # ax = fig.add_subplot(projection='3d')
            # ax.set_title("Professional embeddings\nTopic: \"cool nature-inspired chair\"\nwordnet embedding post t-SNE reduction from 512d to 3d")
            # ax.scatter(X_reduced_3[:, 0], X_reduced_3[:, 1], X_reduced_3[:, 2], marker='o')
            # plt.show()
            # embedding_obj.twod["[gen] 2d embedding"]

            embedding_fig = px.scatter(
                thisVizEmbData.default_embedding_df.twod,
                x="[gen] 2d embedding x",
                y="[gen] 2d embedding y",
                hover_name="[title] TITLE",
                # hover_data=embedding_params.hover_data,
                # title=embedding_params.graph_title,
            )
            st.write(embedding_fig)

    # def visualize_embedding():
    #     embedding_fig = px.scatter(
    #         thisVizEmbData.df,
    #         x=thisVizEmbData.default_embedding_df.twod["2d embedding"][0],
    #         y=thisVizEmbData.default_embedding_df.twod["2d embedding"][1],
    #         hover_name="[title] TITLE",
    #         hover_data=embedding_params.hover_data,
    #         title=embedding_params.graph_title,
    #     )
    #     st.write(embedding_fig)


    # if thisVizEmbData.default_embedding_df is not None:
    #     st.subheader(thisVizEmbData.project_name + " - Default Embedding")
    #     visualize_embedding(thisVizEmbData.default_embedding_df, embedding_params)

