import streamlit as st
from modules.VizEmb import *
import plotly.express as px
import pandas as pd

st.markdown("""
# GRAPH
*visualize correlations in your data using graphs*
""")

if thisVizEmbData.df is None:
    st.success("No data loaded. Please load your database in START.")
else:
    with st.expander("See raw data"):
        st.write(thisVizEmbData.df)
    parameter_list = thisVizEmbData.df.columns.tolist()

    graph_type = st.selectbox("Select graph type", [
        "Quantitative Data / Time",
        "Quantitative Data / Category",
        "Categorical Data / Time", 
        # "Categorical Data / Category", # not implemented
        "Free form"
        ])
    graph_type_prefix_dict = {
        "Quantitative Data / Time": {"x": "[date]", "y": "[quant]"},
        "Quantitative Data / Category": {"x": "[cat]", "y": "[quant]"},
        "Categorical Data / Time": {"x": "[date]", "y": "[cat]"},
        "Categorical Data / Category": {"x": "[cat]", "y": "[cat]"},
        "Free form": {"x": "", "y": ""}
        }

    ### GENERIC GRAPH PARAMETERS ###

    with st.expander("Set graph parameters"):
        graph_title = st.text_input("Enter your graph title:", "Graph Title")
        selected_hover_data = st.multiselect('Hover Data', parameter_list)
        col1, col2 = st.columns(2)

        selected_xdata = col1.selectbox('X Data', [col for col in parameter_list if col.startswith(graph_type_prefix_dict[graph_type]["x"])])
        selected_ydata = col2.multiselect('Y Data', [col for col in parameter_list if col.startswith(graph_type_prefix_dict[graph_type]["y"])])

        regression = st.checkbox('Regression', value=False)
        if regression == True:
            regression_type = st.selectbox('Regression Type', 
                ['Ordinary Least Squares', 
                'Locally Weighted Scatterplot Smoothing',
                'Moving Averages: Rolling',
                'Moving Averages: Exponential',
                'Moving Averages: Expanding'])

    # Types of regressions: https://plotly.com/python/linear-fits/   
    regression_options = {
        'Ordinary Least Squares': ['ols', None], 
        'Locally Weighted Scatterplot Smoothing': ['lowess', dict(frac=0.1)], 
        'Moving Averages: Rolling': ['rolling', dict(window=5)],
        'Moving Averages: Exponential': ['ewm', dict(halflife=2)],
        'Moving Averages: Expanding': ['expanding', None],
        }
    graph_fig = None

    if graph_type == "Quantitative Data / Time" or graph_type == "Quantitative Data / Category":
        graph_fig = px.scatter(
            thisVizEmbData.df,
            x=selected_xdata,
            y=selected_ydata,
            hover_name="[title] TITLE",
            hover_data=selected_hover_data,
            title=graph_title,
            trendline= None if regression != True else regression_options[regression_type][0],
            trendline_options= None if regression != True else regression_options[regression_type][1],
        )
    elif graph_type == "Categorical Data / Time": # or graph_type == "Categorical Data / Category":
        if selected_xdata and selected_ydata:
            with st.spinner("Calculating categorical statistics..."):
                thisVizEmbData.parse_cat_dfs()

                graph_fig = px.bar(
                    thisVizEmbData.parsed_cat_dfs[selected_ydata[0]],
                    x=selected_xdata,
                    y=thisVizEmbData.parsed_cat_dfs[selected_ydata[0]].filter(regex='[catval]').columns,
                    hover_name="[title] TITLE",
                    hover_data=selected_hover_data,
                    title=graph_title,
                )
                st.success("Categorical statistics calculated.")
        

    # st.subheader(graph_title)
    if graph_fig:
        st.write(graph_fig)