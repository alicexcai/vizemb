import streamlit as st
from modules.VizEmb import *
import plotly.express as px
import plotly.graph_objects as go
import tensorflow as tf

from streamlit_plotly_events import plotly_events

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
    # st.write(thisVizEmbData.df)
    
    # FILTER DATA

    # with st.sidebar:
        
    #     thisVizEmbData.filter_df("TITLE")
    #     thisVizEmbData.parse_cat_dfs()
    #     search_params.item_names = st.selectbox("Select item names", thisVizEmbData.filtered_df["TITLE"])
    #     search_params.search_keywords = st.text_input("Search keywords", "")
        
    #     st.write("### Filters")
    #     if st.button("Apply filters"):
    #         # thisVizEmbData.filter_df(search_params.item_names, search_params.search_keywords)
    #         # thisVizEmbData.parse_cat_dfs()
    #         st.success("Filters applied.")

    #     for quantprop in thisVizEmbData.properties["quant"]:
    #         quantprop_value = st.slider(quantprop, float(thisVizEmbData.properties["quant"][quantprop]["min"]), float(thisVizEmbData.properties["quant"][quantprop]["max"]), (float(thisVizEmbData.properties["quant"][quantprop]["min"]), float(thisVizEmbData.properties["quant"][quantprop]["max"])))
    #         search_params.quant_params.append(QuantParam(quantprop, quantprop_value[0], quantprop_value[1]))
    #         # search_params.quant_params.append(QuantParam(quantprop, quantprop_value, quantprop_value))

    #     for catprop in thisVizEmbData.properties["cat"]:
    #         catprop_value = st.selectbox(catprop, thisVizEmbData.cat_values[catprop])
    #         search_params.cat_params.append(CatParam(catprop, catprop_value))
        
    #     st.markdown("---")

        # st.sidebar.slider("Filter by", "TITLE", min_value=0, max_value=len(thisVizEmbData.filtered_df["TITLE"])-1, value=0)

    # EMBEDDING PARAMETERS

    with st.expander("Embedding Parameters"):
        for property in list(thisVizEmbData.properties["quant"].keys()) + list(thisVizEmbData.properties["cat"].keys()) + list(thisVizEmbData.properties["sem"].keys()):
            # if st.checkbox(property, True):
            embedding_params.property_weights[property] = st.slider(property, 0, 10, 1, 1)
        
    
    with st.expander("Visualization Paramters"):
        embedding_params.graph_title = st.text_input("Enter your graph title", "")
        # embedding_params.num_nodes = st.slider("# of Nodes", 1, thisVizEmbData.df.shape[0], 10)
        # embedding_params.mode = st.selectbox("Mode", ["global", "local"])
        embedding_params.color = st.selectbox("Color", ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "black", "white"])
        embedding_params.marker_size = st.slider("Marker Size", 1, 50, 5)
        embedding_params.hover_data = st.multiselect("Select data to display on hover", thisVizEmbData.df.columns.tolist())


    @st.cache
    def generate_default_embeddings():
        with st.spinner("Calculating embeddings..."):
            thisVizEmbData.compose_default_embedding()
            thisVizEmbData.reduce2twod_embedding_df(thisVizEmbData.default_embedding_df, weights = "default")
            st.success("Embeddings generated.")

    # GENERATE EMBEDDINGS
    @st.cache 
    def compose_specified_embedding():
        with st.spinner("Calculating specified embeddings..."):
            thisVizEmbData.compose_default_embedding()
            thisVizEmbData.specified_embedding_df.highdim = thisVizEmbData.default_embedding_df.highdim.copy()
            thisVizEmbData.reduce2twod_embedding_df(thisVizEmbData.specified_embedding_df, embedding_params.property_weights)
            st.success("Specified embeddings generated.")
    
    # initialize session state for generated to false
    if 'generated' not in st.session_state:
        st.session_state.generated = False
    if 'selected_embedding_df' not in st.session_state:
        st.session_state.selected_embedding_df = False

    if st.button("Generate embeddings"):
        generate_default_embeddings()
        st.session_state.selected_embedding_df = thisVizEmbData.default_embedding_df.twod
        st.session_state.generated = True
    if st.button("Generate specified embeddings"):
        compose_specified_embedding()
        st.session_state.selected_embedding_df = thisVizEmbData.specified_embedding_df.twod
        st.session_state.generated = True
        # selected_embedding_df = thisVizEmbData.compose_specified_embedding(embedding_params)

    if st.session_state.generated:
        embedding_fig = px.scatter(
        st.session_state.selected_embedding_df,
        x="[gen] 2d embedding x",
        y="[gen] 2d embedding y",
        hover_name="[title] TITLE",
        hover_data=embedding_params.hover_data,
        color_discrete_sequence=[embedding_params.color]
        # title=embedding_params.graph_title,
        )
        selected_points = plotly_events(embedding_fig, click_event=True)
        # st.write(embedding_fig)
        if selected_points:
            
            with st.expander("Selected Item Details"):
                # st.write(selected_points)
                selected_index = selected_points[0]["pointIndex"]
                selected_itemdata = thisVizEmbData.df.iloc[[selected_index]]
                selected_itemdata_dict = {col: selected_itemdata[col].values[0] for col in selected_itemdata.columns}
                st.write(selected_itemdata)
                st.write(selected_itemdata_dict)


#######################################################################################

    # # def hover_template(hover_data):
    # #     hover_template = ""
    # #     for data in hover_data:
    # #         hover_template = hover_template + "<br>" + data + ": %{value}"
    # #     return hover_template
    # # thisdata = {datacol: thisVizEmbData.default_embedding_df.twod.filter[datacol].tolist() for datacol in embedding_params.hover_data}
    # hover_data_df = thisVizEmbData.default_embedding_df.twod.filter(embedding_params.hover_data)
    # hover_data = ["<br>".join([f"{datacol}: {row[datacol]}" for datacol in hover_data_df.columns]) for index, row in hover_data_df.iterrows()]
    # # print("hover_data:", hover_data)
    # # fig = go.Figure()
    # fig = go.FigureWidget([go.Scatter(
    #     # thisVizEmbData.default_embedding_df.twod,
    #     x=thisVizEmbData.default_embedding_df.twod["[gen] 2d embedding x"],
    #     y=thisVizEmbData.default_embedding_df.twod["[gen] 2d embedding y"],
    #     # hover_name=thisVizEmbData.default_embedding_df.twod["[title] TITLE"],
    #     # hovertemplate =
    #     # "<br>".join(['<b>%{datacol}: {values}</b>' for datacol, values in thisdata.items()]),
    #     # text = ['Custom text {}'.format(i + 1) for i in range(5)],
    #     # text = thisVizEmbData.default_embedding_df.twod.filter[embedding_params.hover_data],
    #     hovertext = hover_data,
    #     # hover_data=embedding_params.hover_data,
    #     # color_discrete_sequence=[embedding_params.color],
    #     mode='markers',
    #     marker=dict(color=embedding_params.color, size=embedding_params.marker_size)
    #     # title=embedding_params.graph_title,
    #     )
    # ])

        # # create our callback function
    # def item_clicked(trace, points, selector):
    #     print("item clicked")
    #     c = list(scatter.marker.color)
    #     s = list(scatter.marker.size)
    #     for i in points.point_inds:
    #         c[i] = '#bae2be'
    #         s[i] = 20
    #         with fig.batch_update():
    #             scatter.marker.color = c
    #             scatter.marker.size = s

    # scatter = fig.data[0]
    # scatter.on_click(item_clicked)

    # st.plotly_chart(fig, use_container_width=True)

    # fig = px.scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])
    # selected_points = plotly_events(fig, click_event=True)
    # st.write(selected_points)







    # thisVizEmbData.default_embedding_df.highdim = pd.read_pickle("/Users/alicecai/Desktop/vizemb/streamlit/default_embedding_df_highdim.pkl")

    # VISUALIZE EMBEDDINGS
            # fig = plt.figure(figsize=(12, 12))
            # ax = fig.add_subplot(projection='3d')
            # ax.set_title("Professional embeddings\nTopic: \"cool nature-inspired chair\"\nwordnet embedding post t-SNE reduction from 512d to 3d")
            # ax.scatter(X_reduced_3[:, 0], X_reduced_3[:, 1], X_reduced_3[:, 2], marker='o')
            # plt.show()
            # embedding_obj.twod["[gen] 2d embedding"]

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

