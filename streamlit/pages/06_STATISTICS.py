from asyncio import selector_events
import streamlit as st
from modules.VizEmb import *

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
        
    # GENERATE STATISICS

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
    
    st.markdown("""
    ### Batch generate statistics
    """)

    selected_batchstats = st.multiselect("Select batch statistics to include", [
        "Category quantitative property averages",
        "Category counts",
    ])
    preset_cat_counts = ["[cat] Form-factor", "[cat] Category of BCI"]
    preset_quantd_counts = ["[quant] Invasiveness", "[quant] Utopianism"]

    if st.button("Generate batch statistics"):
        
        if "Category counts" in selected_batchstats:

            thisVizEmbData.calculate_cat_counts()

            # cat_count_data = defaultdict()
            for preset in preset_cat_counts:
                # cat_count_data[preset] = thisVizEmbData.cat_counts[preset]
                st.write(f"{preset} Counts")
                st.write(thisVizEmbData.cat_counts[preset])

            # quantd_count_data = defaultdict()
            for preset in preset_quantd_counts:
                # quantd_count_data[preset] = thisVizEmbData.calculate_quantd_counts(preset)
                st.write(f"{preset} Counts")
                st.write(thisVizEmbData.calculate_quantd_counts(preset))

        if "Category quantitative property averages" in selected_batchstats:

            preset_categories = {
                "Communication": [
                    "Linking",
                    "Robot control",
                    "Telepathy",
                    "Reading thoughts"
                ],
                "Perception": [
                    "Control of the user",
                    "Emotions",
                    "Memory",
                    "Stimulation",
                    "Storage",
                    "Reality",
                    "Knowledge upload"
                ],
                "Consciousness": [
                    "Dreams",
                    "Transfer",
                    "Termination"
                ],
                "Surveillance": [
                    "Recording",
                    "Tracking",
                    "Advertisement",
                    "Cerebral defense"
                ]
            }

            keyword_map = {
                "Communication": "communication",
                "Linking": "linking",
                "Robot control": "robot",
                "Telepathy": "telepathy",
                "Reading thoughts": "reading",
                "Perception": "perception",
                "Control of the user": "user",
                "Emotions": "emotions",
                "Memory": "memory",
                "Stimulation": "stimulation",
                "Storage": "storage",
                "Reality": "reality",
                "Knowledge upload": "knowledge",
                "Consciousness": "consciousness",
                "Dreams": "dreams",
                "Transfer": "transfer",
                "Termination": "termination",
                "Surveillance": "surveillance",
                "Recording": "recording",
                "Tracking": "tracking",
                "Advertisement": "advertisement",
                "Cerebral defense": "cerebral"
            }

            preset_quantprops = [
                "[quant] Reality factor",
                "[quant] Neurafictionality",
                "[quant] Neuroptimism",
                "[quant] BCI forecast"
            ]
            
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
                    # averages_dict[preset][quantprop] = defaultdict()
                    # st.write("Filter list:", filter_list)
                    quantprop_short = quantprop.replace("[quant]", "").strip()
                    # st.write("Quantprop short:", quantprop_short)
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