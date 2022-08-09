import streamlit as st
from modules.VizEmb import *
from modules import embed

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
    st.code("Your database has been loaded.")

    # preprocess database

    selected_columns = st.multiselect("Select columns to include in your analysis", thisVizEmbData.unprocessed_df.columns)#, list(thisVizEmbData.unprocessed_df.columns))
    column_dict = defaultdict()
    col1, col2, col3 = st.columns(3)
    for i, column in enumerate(selected_columns):
        column_dict[column] = col1.selectbox(f"'{column}' Type", ["id", "title", "img", "date", "sem", "cat", "quant"]) if i % 3 == 0 else col2.selectbox(f"'{column}' Type", ["id", "title", "img", "date", "sem", "cat", "quant"]) if i % 3 == 1 else col3.selectbox(f"'{column}' Type", ["id", "title", "img", "date", "sem", "cat", "quant"]) if i % 3 == 2 else None

    if st.button("Preprocess database"):
        thisVizEmbData.process_df(column_dict)
        st.code("Your database has been preprocessed.")

    st.markdown("---")

    # show database details

    if thisVizEmbData.df is not None:
        
        thisVizEmbData.get_properties()
        thisVizEmbData.split_df()
        thisVizEmbData.parse_cat_dfs()

        st.markdown("""### Quantitative data""")
        st.write(thisVizEmbData.properties["quant"])
        st.write(thisVizEmbData.quant_df)
        st.markdown("""### Categorical data""")
        st.write(thisVizEmbData.properties["cat"])
        st.write(thisVizEmbData.cat_df)
        st.markdown("""### Semantic data""")
        st.write(thisVizEmbData.properties["sem"])
        st.write(thisVizEmbData.sem_df)
        st.markdown("""### Full database""")
        st.write(thisVizEmbData.df)

