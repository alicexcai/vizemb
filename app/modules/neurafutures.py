import streamlit as st
from collections import defaultdict
import yaml
import numpy as np
import re

# load NEURAFUTURES config file

with open("modules/config.yml") as f:
    configData = yaml.safe_load(f)

def neurafuture_preprocessing(df):

    processed_df = df.copy()
    processed_df.columns = processed_df.columns.str.replace(r'(^.*Title.*$)', "[title] TITLE")
    # st.write(processed_df.columns)
    # processed_df = processed_df.replace("<NA>", np.nan, inplace=True, regex=True)
    processed_df.rename(columns=configData["columnMap"], inplace=True)
    processed_df = processed_df.filter(items=list(configData["columnMap"].values()))
    processed_df["[date] DATE"] = processed_df["[quant] Date"]
    # replace keywords with corresponding flotts from dictionary
    processed_df = processed_df.replace(np.nan, "None")
    
    # loop through image column and split string
    for i in range(len(processed_df["[img] Cover Image"])):
        if processed_df["[img] Cover Image"][i] != "None":
            processed_df.at[i, "[img] Cover Image"] = "imgs/" + processed_df.iloc[i]["[img] Cover Image"].split("/")[-1]

    for quant_prop in processed_df.filter(regex="quant|date").columns:
        # st.write("processing quant prop:", quant_prop)
        processed_df.replace({quant_prop: {"None": 0.5}}, inplace=True)
    for quantd_prop in configData["discreteQuantProps"]:

        # astype(float)
        # processed_df[quantd_prop] = processed_df[quantd_prop].replace(np.nan,0.5,regex=True)
        # st.write(processed_df[quantd_prop])
        # st.write(processed_df)
        # st.write(quantd_prop)
        # st.write(processed_df.iloc[2]["[cat] Form-factor"])
        # st.write(type(processed_df.iloc[2]["[cat] Form-factor"]))
        # processed_df[quantd_prop] = processed_df[quantd_prop].astype(str)
        # processed_df1 = processed_df.replace(np.nan, "None")
        # st.write(processed_df)
        processed_df = processed_df.replace({quantd_prop: configData["discreteQuantProps"][quantd_prop]})
        processed_df[quantd_prop] = processed_df[quantd_prop].astype(float)
        # processed_df[quantd_prop] = processed_df[quantd_prop].astype(float)
        
    # st.write(processed_df)
    processed_df = processed_df[configData["columnOrder"]]
    return processed_df
    
def neurafutures_batchstats(thisVizEmbData):

    st.markdown("""
    ### Batch generate statistics
    """)

    selected_batchstats = st.multiselect("Select batch statistics to include", configData["batchStats"])
    preset_cat_counts = configData["presetCatCounts"]
    preset_quantd_counts = configData["presetQuantdCounts"]

    if st.button("Generate batch statistics"):
        
        if "# of Items / Category" in selected_batchstats:

            thisVizEmbData.calculate_cat_counts()

            for preset in preset_cat_counts:
                st.write(f"{preset} Counts")
                st.write(thisVizEmbData.cat_counts[preset])

            for preset in preset_quantd_counts:
                st.write(f"{preset} Counts")
                st.write(thisVizEmbData.calculate_quantd_counts(preset))

        if "Average Values / Category" in selected_batchstats:

            preset_categories = configData["presetCategories"]
            keyword_map = configData["keywordMap"]
            preset_quantprops = configData["presetQuantProps"]
            
            st.markdown("""
            ### Averages by Category
            """)
            averages_dict = defaultdict()
            length_dict = defaultdict()

            for preset in preset_categories:
                averages_dict[preset] = defaultdict()
                length_dict[preset] = defaultdict()
                filter_list = [keyword_map[item] for item in [preset] + preset_categories[preset]]
                filtered_df = thisVizEmbData.filter_df({"[cat] Category of BCI": filter_list})
                length_dict[preset]["Total"] = len(filtered_df)
                for quantprop in preset_quantprops:
                    quantprop_short = quantprop.replace("[quant]", "").strip()
                    mean = filtered_df.filter(regex=quantprop_short)[quantprop].mean()
                    averages_dict[preset][quantprop] = mean

                for item in filter_list:
                    averages_dict[preset][item] = defaultdict()
                    filtered_df = thisVizEmbData.filter_df({"[cat] Category of BCI": [item]})
                    length_dict[preset][item] = len(filtered_df)
                    for quantprop in preset_quantprops:
                        quantprop_short = quantprop.replace("[quant]", "").strip()
                        mean = filtered_df.filter(regex=quantprop_short)[quantprop].mean()
                        averages_dict[preset][item][quantprop] = mean

                with st.expander(f"{preset} Filtered df:"):
                    st.write(filtered_df)

            st.write(averages_dict)
            st.write(length_dict)