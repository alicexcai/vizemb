import streamlit as st
from modules.VizEmb import *
from modules import embed, neurafutures

st.markdown("""
## GETTING STARTED
Load your database to get started. Make sure your database follows the specified schema. Label your columns with the correct types.
""")

# load database

thisVizEmbData.project_name = st.text_input("Enter your project name:", thisVizEmbData.project_name)
uploaded_file = st.file_uploader("Upload database", type = ['csv']) # , 'xlsx', 'sqlite', 'db'])

if uploaded_file:
    thisVizEmbData.save_db_file(uploaded_file)
    
    thisVizEmbData.load_df()
    st.success("Your database has been loaded.")

    # preprocess database

    # special preprocessing for NEURAFUTURES
    thisVizEmbData.df = neurafutures.neurafuture_preprocessing(thisVizEmbData.unprocessed_df)
    st.success("Your database has been preprocessed.")

    # if st.radio("Select preprocessing method", ["manual", "neurafutures"], index=1) == "neurafutures":
    #     thisVizEmbData.df = neurafutures.neurafuture_preprocessing(thisVizEmbData.unprocessed_df)
    #     st.success("Your database has been preprocessed.")
        
    # else:
    #     selected_columns = st.multiselect("Select columns to include in your analysis", thisVizEmbData.unprocessed_df.columns)#, list(thisVizEmbData.unprocessed_df.columns))
    #     column_dict = defaultdict()
    #     col1, col2, col3 = st.columns(3)
    #     for i, column in enumerate(selected_columns):
    #         column_dict[column] = col1.selectbox(f"'{column}' Type", ["id", "title", "date", "img", "sem", "cat", "quant"]) if i % 3 == 0 else col2.selectbox(f"'{column}' Type", ["id", "title", "img", "date", "sem", "cat", "quant"]) if i % 3 == 1 else col3.selectbox(f"'{column}' Type", ["id", "title", "img", "date", "sem", "cat", "quant"]) if i % 3 == 2 else None

    #     if st.button("Preprocess database"):
    #         thisVizEmbData.process_df(column_dict)
    #         st.success("Your database has been preprocessed.")

    st.markdown("---")

    # show database details

    if thisVizEmbData.df is not None:
        
        thisVizEmbData.get_properties()
        thisVizEmbData.split_df()
        thisVizEmbData.parse_cat_dfs()

        with st.expander("View quantitative data"):
            st.markdown("""### Quantitative data""")
            st.write(thisVizEmbData.properties["quant"])
            st.write(thisVizEmbData.quant_df)
        with st.expander("View categorical data"):
            st.markdown("""### Categorical data""")
            st.write(thisVizEmbData.properties["cat"])
            st.write(thisVizEmbData.cat_df)
        with st.expander("View semantic data"):
            st.markdown("""### View semantic data""")
            st.write(thisVizEmbData.properties["sem"])
            st.write(thisVizEmbData.sem_df)
        with st.expander("View full database"):
            st.markdown("""### Full database""")
            st.write(thisVizEmbData.df)

