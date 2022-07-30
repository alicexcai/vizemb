import streamlit as st
from modules.VizEmb import *
from wordcloud import WordCloud
import matplotlib.pyplot as plt

### PAGE SETUP ###

st.markdown("""
# SEMANTICS
*visualize the semantic properties of your data*
""")

if thisVizEmbData.df is None:
    st.success("No data loaded. Please load your database in START.")
else:

    # VISUALIZATioN PARAMETERS
    
    thisVizEmbData.filter_df("TITLE")
    thisVizEmbData.parse_cat_dfs()
    visualization_items = st.multiselect("Select item names", thisVizEmbData.filtered_df["TITLE"])
    max_word = st.slider("Max words", 5, 500, 100)
    max_font = st.slider("Max Font Size", 10, 100, 50)
    bg_color = st.selectbox("Background Color", ["white", "black"])
    color_map = st.selectbox("Color Map", ["viridis", "plasma", "inferno", "magma", "cividis"])

    if visualization_items == []:
        st.success("No item selected. Please select item(s) to visualize.")
    else:

        # get descriptions
        items_df = thisVizEmbData.df.loc[thisVizEmbData.df["[title] TITLE"].isin(visualization_items)]
        items_descriptions = {title : description for title, description in zip(items_df["[title] TITLE"], items_df["[sem] Description"])}
        for title, description in items_descriptions.items():
            with st.expander(title):
                st.write(description)
        items_descriptions_concat = " ".join(items_descriptions.values())

        # generate a word cloud image:
        wordcloud = WordCloud(background_color=bg_color, colormap=color_map, max_words=max_word, max_font_size=max_font).generate(items_descriptions_concat)
        fig, ax = plt.subplots()
        plt.axis("off")
        ax.imshow(wordcloud, interpolation='bilinear')
        st.pyplot(fig)

        

