import streamlit as st
from modules.VizEmb import *

st.markdown("""
## GETTING STARTED
Load your database to get started. Make sure your database follows the specified schema. Label your columns with the correct types.
""")

thisVizEmbData.project_name = st.text_input("Enter your project name:", thisVizEmbData.project_name)

# uploaded_file = st.file_uploader("Upload data", type = ['csv']) # , 'xlsx', 'sqlite', 'db'])

### TEMP FOR DEVELOPMENT ###
uploaded_file = True
thisVizEmbData.db_file = "/Users/alicecai/Downloads/Database.csv"
### TEMP FOR DEVELOPMENT ###

# save uploaded file to global data state
if uploaded_file:
    # thisVizEmbData.save_db_file(uploaded_file)
    thisVizEmbData.load_df()
    st.code("Your database has been loaded.")

# if thisVizEmbData.db_file:
#     st.download_button(
#         thisVizEmbData.db_filename,
#         thisVizEmbData.df.to_csv().encode('utf-8'),
#         "Database.csv",
#         "text/csv",
#         key='download-csv')
    
    thisVizEmbData.get_properties()
    thisVizEmbData.split_df()
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

