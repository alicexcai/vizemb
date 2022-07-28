# generates and integrates embeddings for all data

from embeddings.embed_quant import *
from embeddings.embed_sem import *
from classes import Item, Database

import pandas as pd
import numpy as np

class InputParams:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

database_params = InputParams(
    original_data_name="NeuraFutures (original)",
    original_data_path = "data/original_data.csv",
    processed_data_name="NeuraFutures (processed)",
    processed_data_path = "data/processed_data.csv",
    )

# specified embedding weights dict
specified_embedding_weights = {
    # property : weight
}

embedding_params = InputParams(
    embedding_type="default", # "default" or "specified"
    embedding_weights=None
)

def generate_embeddings(database_params, embedding_params):
    
    # load data

    original_db = Database(database_params.original_data_name, database_params.original_data_path)

    
    # # clean up data

    # # generate embeddings
    # df = embed_quant(data, embedding_type, embedding_params)
    
    # # save embeddings

    # df.to_csv(embedding_file, index=False)
    
    # return df

# sem_embedding_df = load_data('data/sem_embedding.csv')

generate_embeddings('data/original_data.csv', 'data/processed_data.csv')