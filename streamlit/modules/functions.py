# import openai
# import os
# from dotenv import load_dotenv
# load_dotenv()

# def ai_embed(text, model="text-similarity-davinci-001"):
#     openai.api_key= os.getenv("OPENAI_API_KEY")
#     text = text.replace("\n", " ")
#     return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']

import spacy
import tensorflow as tf
import tensorflow_hub as hub

sp = spacy.load('en_core_web_sm')
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)
print("module %s loaded" % module_url)

def ai_embed(text):
    return model(text)
