import tensorflow_hub as hub
import streamlit as st 
from modules.VizEmb import *

# add generated status to session state

if 'generated' not in st.session_state:
    st.session_state.generated = False

# load semantic embedding models

@st.cache
def load_model():
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    model = hub.load(module_url)
    print("module %s loaded" % module_url)
    return model
model = load_model()

# embed text

def ai_embed(text):
    return model(text)

# generate default embeddings

@st.cache
def generate_default_embeddings(thisVizEmbData):
    thisVizEmbData.compose_default_embedding()
    thisVizEmbData.reduce2twod_embedding_df(thisVizEmbData.default_embedding_df, weights = "default")
    thisVizEmbData.reduce2oned_embedding_df()
    st.session_state.generated = True

# generate specific embeddings

@st.cache 
def compose_specified_embedding(thisVizEmbData, embedding_params):
    thisVizEmbData.compose_default_embedding()
    thisVizEmbData.specified_embedding_df.highdim = thisVizEmbData.default_embedding_df.highdim.copy()
    thisVizEmbData.reduce2twod_embedding_df(thisVizEmbData.specified_embedding_df, embedding_params.property_weights)
    st.session_state.generated = True