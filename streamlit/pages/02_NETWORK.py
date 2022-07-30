import streamlit as st
from modules.VizEmb import *
import plotly.express as px

from streamlit_plotly_events import plotly_events

embedding_params = Params(
    property_weights = {},
    color = None,
)

### PAGE SETUP ###

st.markdown("""
# NETWORK
*visualize your data in a shared embedding space*
""")

if thisVizEmbData.df is None:
    st.success("No data loaded. Please load your database in START.")
else:

    # EMBEDDING PARAMETERS

    with st.expander("Embedding Parameters"):
        for property in list(thisVizEmbData.properties["quant"].keys()) + list(thisVizEmbData.properties["cat"].keys()) + list(thisVizEmbData.properties["sem"].keys()):

            embedding_params.property_weights[property] = st.slider(property, 0, 10, 1, 1)
        
    
    with st.expander("Visualization Paramters"):
        embedding_params.graph_title = st.text_input("Enter your graph title", "")

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

        if selected_points:
            
            with st.expander("Selected Item Details"):

                selected_index = selected_points[0]["pointIndex"]
                selected_itemdata = thisVizEmbData.df.iloc[[selected_index]]
                selected_itemdata_dict = {col: selected_itemdata[col].values[0] for col in selected_itemdata.columns}
                st.write(selected_itemdata)
                st.write(selected_itemdata_dict)
