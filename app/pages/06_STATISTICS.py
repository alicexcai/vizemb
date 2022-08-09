import streamlit as st
from modules.VizEmb import *
from modules import neurafutures

st.markdown("""
# STATISTICS
*perform statistical analyses on your data*
""")

if thisVizEmbData.df is None:
    st.success("No data loaded. Please load your database in START.")
else:
    parameter_list = thisVizEmbData.df.columns.tolist()
    thisVizEmbData.parse_cat_dfs()

    with st.expander("See raw data"):
        st.write(thisVizEmbData.df)

    with st.expander("Generate custom statistics"):
        selected_quantprops = st.multiselect("Select properties to generate statistics for", thisVizEmbData.properties["quant"])
        params = defaultdict()
        for catprop in thisVizEmbData.properties["cat"]:
            catprop_value = st.multiselect(catprop, thisVizEmbData.cat_values[catprop], default=thisVizEmbData.cat_values[catprop])
            params[catprop] = catprop_value
        
    # generate statistics

        if st.button("Generate custom statistics"):
            filtered_df = thisVizEmbData.filter_df(params)
            st.write(filtered_df)
            statistics = defaultdict()
            for prop in selected_quantprops:
                statistics[prop] = {
                    "mean": filtered_df[prop].mean(),
                    "std": filtered_df[prop].std(),
                    "min": filtered_df[prop].min(),
                    "max": filtered_df[prop].max(),
                }
                
            st.write(statistics)

    # generate batch statistics specific to NEURAFUTURES

    neurafutures.neurafutures_batchstats(thisVizEmbData)