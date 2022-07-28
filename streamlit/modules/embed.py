import spacy
import tensorflow as tf
import tensorflow_hub as hub
import streamlit as st

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