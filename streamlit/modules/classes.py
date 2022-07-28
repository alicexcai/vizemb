# defining a database class to store db info and an object class for each item in the database
import pandas as pd

class Database:
    def __init__(self, name, file_path, **kwargs):
        # self.__dict__.update(kwargs) # only if necessary
        self.name = name
        self.file_path = file_path
        self.df = pd.read_csv(file_path, encoding = "ISO-8859-1") # threw error with utf-8
        self.quant_df = None
        self.sem_df = None
        self.quant_embedding_df = None
        self.sem_embedding_df = None
        self.default_embedding_df = None
        self.specified_embedding_df = None

    def __repr__(self):
        return f"{self.name} ({self.file_path})"

    def split_quant_sem(self):
        # split quantitative and semantic data
        self.quant_df = self.df[self.df.columns[:-1]]
        self.sem_df = self.df[self.df.columns[-1]]

    def calculate_quant_embedding(self):
        # calculate quantitative embedding and output embedding df
        # this is simply normalization of the quantitative data from 0 to 1
        return self.quant_embedding_df

    def calculate_sem_embedding(self):
        # calculate semantic embedding and output embedding df
        return self.sem_embedding_df

    def compose_default_embedding(self):
        # calculate composite embedding by combining quantitative and semantic embeddings
        return self.default_embedding_df
    
    def compose_specified_embedding(self, weights):
        # calculate composite embedding by combining weighted quantitative and semantic embeddings
        return self.specified_embedding_df


# items derived from database at runtime?
class Item:
    def __init__(self, name, id, **kwargs):
        # self.__dict__.update(kwargs) # only if necessary
        self.name = name
        self.id = id
        self.original_data = None
        self.processed_data = None
        self.quant_embedding = None
        self.sem_embedding = None
        self.default_embedding = None
        self.specified_embedding = None
        self.__dict__.update(kwargs)

    def __repr__(self):
        return f"{self.name} ({self.id})"

    def fetch_original_data(self, original_df):
        # get original data from original database
        return self.original_data

    def fetch_processed_data(self, processed_df):
        # get processed data from processed database
        return self.processed_data

    def fetch_sem_embedding(self, sem_embedding_df):
        # get semantic embedding from semantic embedding database
        return self.sem_embedding

    def fetch_quant_embedding(self):
        # get quantitative embedding from quantitative embedding database
        return self.quant_embedding

    def fetch_default_embedding(self):
        # get composite embedding from default embedding database
        return self.default_embedding
    
    def fetch_specified_embedding(self, weights):
        # get composite embedding from specified embedding database
        return self.specified_embedding