import streamlit as st
from modules.VizEmb import *

st.markdown("""
# STATISTICS
*perform statistical analyses on your data*
""")

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

if thisVizEmbData.df is None:
    st.success("No data loaded. Please load your database in START.")
else:
    parameter_list = thisVizEmbData.df.columns.tolist()

    with st.expander("See raw data"):
        st.write(thisVizEmbData.df)

    with st.expander("Statistics parameters"):
        selected_quantprops = st.multiselect("Select properties to generate statistics for", thisVizEmbData.properties["quant"])
        # selected_quantstats = st.multiselect("Select statistics to generate", ["mean", "std", "min", "max"])

    # GENERATE STATISICS

    # with st.sidebar:
        
    #     thisVizEmbData.get_colvalues("TITLE")
    thisVizEmbData.parse_cat_dfs()
    #     search_params.item_names = st.selectbox("Select item names", thisVizEmbData.colvalue_df["TITLE"])
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

    # with st.expander()
    params = defaultdict()
    for catprop in thisVizEmbData.properties["cat"]:
        # if st.checkbox("Select all", key=catprop):
        #     selected_catprop_values = thisVizEmbData.cat_values[catprop]
        catprop_value = st.multiselect(catprop, thisVizEmbData.cat_values[catprop], default=thisVizEmbData.cat_values[catprop])
        params[catprop] = catprop_value
    
    if st.button("Generate statistics"):
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

    