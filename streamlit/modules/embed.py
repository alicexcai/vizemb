import spacy
import tensorflow as tf
import tensorflow_hub as hub
import streamlit as st 
from modules.VizEmb import *

if 'generated' not in st.session_state:
    st.session_state.generated = False

@st.cache
def load_model():
    sp = spacy.load('en_core_web_sm')
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    model = hub.load(module_url)
    print("module %s loaded" % module_url)
    return model
model = load_model()

def ai_embed(text):
    return model(text)

@st.cache
def generate_default_embeddings(thisVizEmbData):
    with st.spinner("Calculating embeddings..."):
        thisVizEmbData.compose_default_embedding()
        thisVizEmbData.reduce2twod_embedding_df(thisVizEmbData.default_embedding_df, weights = "default")
        thisVizEmbData.reduce2oned_embedding_df()
        st.success("Embeddings generated.")
        st.session_state.generated = True

@st.cache 
def compose_specified_embedding(thisVizEmbData, embedding_params):
    with st.spinner("Calculating specified embeddings..."):
        thisVizEmbData.compose_default_embedding()
        thisVizEmbData.specified_embedding_df.highdim = thisVizEmbData.default_embedding_df.highdim.copy()
        thisVizEmbData.reduce2twod_embedding_df(thisVizEmbData.specified_embedding_df, embedding_params.property_weights)
        st.success("Specified embeddings generated.")
        st.session_state.generated = True