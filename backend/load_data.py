# load data from data folder

import pandas as pd
import numpy as np

# load data

def load_data(data_file):
    data = pd.read_csv(data_file)
    return data

original_df = pd.read_csv('data/original_data.csv')
processed_df = pd.read_csv('data/processed_data.csv')
sem_embedding_df = pd.read_csv('data/sem_embedding.csv')

# clean up data

# find similarities

df = pd.read_csv('output/embedded_1k_reviews.csv')
df['babbage_similarity'] = df.babbage_similarity.apply(eval).apply(np.array)
df['babbage_search'] = df.babbage_search.apply(eval).apply(np.array)