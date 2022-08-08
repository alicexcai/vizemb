import streamlit as st
from modules.VizEmb import *
from modules import embed

st.markdown("""
## GETTING STARTED
Load your database to get started. Make sure your database follows the specified schema. Label your columns with the correct types.
""")

thisVizEmbData.project_name = st.text_input("Enter your project name:", thisVizEmbData.project_name)

uploaded_file = st.file_uploader("Upload data", type = ['csv']) # , 'xlsx', 'sqlite', 'db'])

# ### TEMP FOR DEVELOPMENT ###
# uploaded_file = True
# thisVizEmbData.db_file = "/Users/alicecai/Downloads/Database.csv"
# ### TEMP FOR DEVELOPMENT ###

# save uploaded file to global data state
if uploaded_file:
    thisVizEmbData.save_db_file(uploaded_file)
    
    thisVizEmbData.load_df()
    st.code("Your database has been loaded.")

    # begin preprocessing process
    selected_columns = st.multiselect("Select columns to include in your analysis", thisVizEmbData.unprocessed_df.columns)#, list(thisVizEmbData.unprocessed_df.columns))
    column_dict = defaultdict()
    col1, col2, col3 = st.columns(3)
    for i, column in enumerate(selected_columns):
        # col1.text_input(f"New title for column '{column}'", "") if i % 4 == 0 else col2.text_input(f"New title for column '{column}'", "") if i % 4 == 1 else col3.text_input(f"New title for column '{column}'", "") if i % 4 == 2 else col4.text_input(f"New title for column '{column}'", "")
        column_dict[column] = col1.selectbox(f"'{column}' Type", ["id", "title", "img", "date", "sem", "cat", "quant"]) if i % 3 == 0 else col2.selectbox(f"'{column}' Type", ["id", "title", "img", "date", "sem", "cat", "quant"]) if i % 3 == 1 else col3.selectbox(f"'{column}' Type", ["id", "title", "img", "date", "sem", "cat", "quant"]) if i % 3 == 2 else None

    if st.button("Pre-process database"):
        thisVizEmbData.process_df(column_dict)
        st.code("Your database has been pre-processed.")

# if thisVizEmbData.db_file:
#     st.download_button(
#         thisVizEmbData.db_filename,
#         thisVizEmbData.df.to_csv().encode('utf-8'),
#         "Database.csv",
#         "text/csv",
#         key='download-csv')

    st.markdown("---")

    if thisVizEmbData.df is not None:
        
        thisVizEmbData.get_properties()
        thisVizEmbData.split_df()
        thisVizEmbData.parse_cat_dfs()

        # if st.button("Generate embeddings"):
        #     embed.generate_default_embeddings(thisVizEmbData)

        # if st.button("Generate embeddings"):
        #     @st.cache
        #     def generate_default_embeddings():
        #         with st.spinner("Calculating embeddings..."):
        #             thisVizEmbData.compose_default_embedding()
        #             thisVizEmbData.reduce2oned_embedding_df()
        #             st.success("Embeddings generated.")

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

