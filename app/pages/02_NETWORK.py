import streamlit as st
from modules.VizEmb import *
import plotly.express as px
from modules import embed
from streamlit_plotly_events import plotly_events

st.markdown("""
# NETWORK
*Explore connections between items in your database using a shared embedding space.*
""")

if thisVizEmbData.df is None:
    st.success("No data loaded. Please load your database in START.")
else:
    with st.expander("See raw data"):
        st.write(thisVizEmbData.df)

    # set embedding parameters

    embedding_params = Params(
    property_weights = {},
    color = None,
    )

    with st.expander("Embedding Parameters"):
        for property in list(thisVizEmbData.properties["quant"].keys()) + list(thisVizEmbData.properties["cat"].keys()) + list(thisVizEmbData.properties["sem"].keys()):
            embedding_params.property_weights[property] = st.slider(property, 0, 10, 1, 1)
    
    with st.expander("Visualization Paramters"):
        embedding_params.graph_title = st.text_input("Enter your graph title", "")
        embedding_params.color = st.selectbox("Color", ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "black", "white"])
        embedding_params.marker_size = st.slider("Marker Size", 1, 50, 5)
        embedding_params.hover_data = st.multiselect("Select data to display on hover", thisVizEmbData.df.columns.tolist())

    if 'selected_embedding_df' not in st.session_state or st.session_state.selected_embedding_df is None:
        st.session_state.selected_embedding_df = False
        st.session_state.generated = False

    if st.session_state.generated == False:
        embed.generate_default_embeddings(thisVizEmbData)

    # generate embeddings

    if st.button("Generate specified embeddings"):
        embed.generate_specified_embedding(thisVizEmbData, embedding_params)
        st.session_state.selected_embedding_df = thisVizEmbData.specified_embedding_df.twod
        st.session_state.generated = True
    else:
        st.session_state.selected_embedding_df = thisVizEmbData.default_embedding_df.twod

    # display embeddings

    if st.session_state.generated == True:
        with st.expander("View embedding values"):
            st.write(st.session_state.selected_embedding_df[["[title] TITLE", "[gen] 2d embedding x", "[gen] 2d embedding y"]])
        embedding_fig = px.scatter(
        st.session_state.selected_embedding_df,
        x="[gen] 2d embedding x",
        y="[gen] 2d embedding y",
        hover_name="[title] TITLE",
        hover_data=embedding_params.hover_data,
        color_discrete_sequence=[embedding_params.color]
        )
        selected_points = plotly_events(embedding_fig, click_event=True)

        if selected_points:
            with st.expander("Selected Item Details"):
                selected_index = selected_points[0]["pointIndex"]
                selected_itemdata = thisVizEmbData.df.iloc[[selected_index]]
                selected_itemdata_dict = {col: selected_itemdata[col].values[0] for col in selected_itemdata.columns}
                st.write(selected_itemdata)
                st.write(selected_itemdata_dict)
                try:
                    st.image(thisVizEmbData.df.filter(regex="img").iloc[selected_index].values[0])
                except:
                    pass
