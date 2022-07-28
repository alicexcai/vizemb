# from classes import Item, Database
import pandas as pd
import numpy as np
from collections import defaultdict
from .embed import ai_embed
import ast
from sklearn.manifold import TSNE

import warnings
warnings.filterwarnings('ignore')

class EmbeddingDf:
    def __init__(self):
        self.highdim = None
        self.expanded = None
        self.reduced = None
        self.twod = None

    
class VizEmbData:
    def __init__(self, **kwargs):
        # self.__dict__.update(kwargs) # only if necessary
        self.project_name = ""
        self.db_file = None
        self.db_filename = None
        self.df = None
        self.filtered_df = defaultdict()
        self.info_df = None
        self.quant_df = None
        self.sem_df = None
        self.cat_df = None
        self.properties = defaultdict() # { quant: {property: {min: , max: , avg: }}, sem: {}, cat: {} }
        
        # move categorical data into properties nested dictionary
        self.cat_values = defaultdict() # {cat_name1 : [cat_value1, cat_value2, ...], cat_name2 ...}
        self.parsed_cat_dfs = defaultdict() # {cat_name1 : parsed_cat1_df, cat_name2 : parsed_cat2_df, ...}
        self.cat_counts = defaultdict() # {cat_name1 : {cat_value1: #, cat_value2: #, ...}, cat_name2 ...}
        
        self.sem_embedding_length = None
        self.quant_embedding_df = None
        self.sem_embedding_df = None
        # self.default_embedding_df = None
        # self.specified_embedding_df = None
        # self.reduced_embedding_df = None
        self.default_embedding_df = EmbeddingDf()
        self.specified_embedding_df = EmbeddingDf()

    def __repr__(self):
        return f"{self.name} ({self.file_path})"

    def save_db_file(self, file):
        try:
            self.db_file = file
            self.db_filename = file.name
        except:
            raise Exception(f"Could not save {file} as db_file")

    def load_df(self):
        try:
            self.df = pd.read_csv(self.db_file, encoding = "ISO-8859-1") # threw error with utf-8
        except:
            raise Exception(f"Could not load data from {self.db_file}")

    def split_df(self):
        # split semantic, categorical, and quantitative
        self.info_df = self.df.filter(regex='id|title|date|info')
        self.quant_df = self.df.filter(regex='quant|id|title|date')
        self.sem_df = self.df.filter(regex='sem|id|title|date')
        self.cat_df = self.df.filter(regex='cat|id|title|date')
    
    def get_properties(self):
        # get list of properties from df
        self.properties["quant"] = {prop : None for prop in self.df.filter(regex='quant').columns.tolist()}
        for quantprop in self.properties["quant"]:
            self.properties["quant"][quantprop] = {"min": self.df.filter(regex=quantprop.replace("[quant]", ""))[quantprop].min(), "max": self.df.filter(regex=quantprop.replace("[quant]", ""))[quantprop].max(), "avg": self.df.filter(regex=quantprop.replace("[quant]", ""))[quantprop].mean()}

        self.properties["sem"] = {prop : None for prop in self.df.filter(regex='sem').columns.tolist()}
        self.properties["cat"] = {prop : None for prop in self.df.filter(regex='cat').columns.tolist()}

    def parse_cat_dfs(self):
        # parse categorical data into dataframe of 1s and 0s 
        # replace nans with strings
        self.cat_df = self.cat_df.replace(np.nan,"None",regex=True)
        for cat_name in self.properties["cat"]:
            # print("cat_name:", cat_name)
            counted_df = self.df.filter(regex='id|title|date')
            # find unique category values
            concat_cat_values = ','.join(self.cat_df[cat_name].astype(str))
            all_cat_values = [x.strip() for x in concat_cat_values.split(',')]
            self.cat_values[cat_name] = list(set(all_cat_values))
            # creates a column for each category value
            for cat_value in self.cat_values[cat_name]:
                for index in range(len(counted_df)):
                    # check if the category value is in the list of category values in the category column
                    counted_df.at[index, "[catval] " + cat_value] = 1 if cat_value in self.cat_df.at[index, cat_name] else 0
            # add category count dfs to dictionary, keyed by category name
            self.parsed_cat_dfs[cat_name] = counted_df
        # print("parsed_cat_dfs: ", self.parsed_cat_dfs)
    
    def calculate_cat_counts(self):
        # calculate categorical counts by property filter
        for cat in self.properties["cat"]:
            for cat_value in self.cat_values[cat]:
                # self.cat_counts[cat].append(self.df[self.df[cat] == cat_value].shape[0])
                self.cat_counts[cat][cat_value] = self.cat_df[cat][cat_value == 1].shape[0]
    
    def filter_df(self, property_filter):
        # filter df by property filter
        self.filtered_df[property_filter] = self.df.filter(regex=property_filter)

    def search_df(self, search_params):
        # search df by search params
        return self.df.query(search_params)

    def calculate_quant_embedding(self):
        # calculate quantitative embedding and output embedding df
        # this is simply normalization of the quantitative data from 0 to 1
        # one column contains concatenated embedding, others contain normalized data
        self.quant_embedding_df = self.quant_df.copy()
        for prop in self.properties["quant"]:
            self.quant_embedding_df[prop] = self.quant_df[prop] / self.properties["quant"][prop]["max"]
        # loop through items in dataframe and concatenate the float values in each column into a single array
        self.quant_embedding_df["quant_embedding"] = None
        self.quant_embedding_df["quant_embedding"] = self.quant_embedding_df["quant_embedding"].astype("object")
        for index in range(len(self.quant_embedding_df)):
            self.quant_embedding_df.at[index, "quant_embedding"] = self.quant_embedding_df.filter(regex="quant").iloc[index, :].to_numpy()
        # print("quant_embedding_df: ", self.quant_embedding_df)
        

    def calculate_sem_embedding(self):
        # calculate semantic embedding and output embedding df
        self.sem_embedding_df = self.df.copy()
        # loop through items in dataframe and replace column text with semantic embedding
        self.sem_embedding_df["sem_embedding"] = None
        self.sem_embedding_df["sem_embedding"] = self.sem_embedding_df["sem_embedding"].astype("object")
        for index in range(len(self.sem_embedding_df)):
            for prop in list(self.properties["sem"].keys()) + list(self.properties["cat"].keys()):
                self.sem_embedding_df.at[index, prop] = ai_embed([str(self.sem_embedding_df.iloc[index][prop])])
                if self.sem_embedding_length == None:
                    self.sem_embedding_length = self.sem_embedding_df.at[index, prop][0].shape[0]
            # concatenate the float values in each column into a single array
            self.sem_embedding_df.at[index, "sem_embedding"] = self.sem_embedding_df.filter(regex="sem|cat").iloc[index, :].to_numpy()
        # print("sem_embedding_df: ", self.sem_embedding_df)

    def compose_default_embedding(self):
        # calculate composite embedding by combining quantitative and semantic embeddings
        self.calculate_quant_embedding()
        self.calculate_sem_embedding()
        self.default_embedding_df.highdim = self.df.copy()
        for index in range(len(self.df)):

            for prop in self.properties["quant"]:
                self.default_embedding_df.highdim.at[index, prop] = self.quant_embedding_df.iloc[index][prop]
            for prop in list(self.properties["sem"].keys()) + list(self.properties["cat"].keys()):
                self.default_embedding_df.highdim.at[index, prop] = self.sem_embedding_df.iloc[index][prop][0].numpy()
            self.default_embedding_df.highdim.at[index, "[gen] composite_embedding"] = self.default_embedding_df.highdim.filter(regex="sem|cat").iloc[index, :].to_numpy()
        # print("FINAL default_embedding_df.highdim: ", self.default_embedding_df.highdim)
        # self.default_embedding_df.highdim.to_pickle("default_embedding_df_highdim.pkl")

    def compose_specified_embedding(self, weights):
        # calculate composite embedding by combining weighted quantitative and semantic embeddings
        return self.specified_embedding_df

    def expand_embedding(self, embedding_obj):
        # pad embedding with constant values to make it consistent in length in all dimensions
        if type(embedding_obj) != EmbeddingDf:
            raise TypeError("embedding_obj must be of type EmbeddingDf")
        else:
            embedding_obj.expanded = self.default_embedding_df.highdim.copy()
            target_length = self.sem_embedding_length
            # target_length = self.sem_embedding_df.iloc[0]["sem_embedding"][0].numpy()[0].shape[0]
            print("TARGET LENGTH: ", target_length)
            for quant_prop in self.properties["quant"]:
                # embedding_obj.expanded[quant_prop] = None
                for index in range(len(embedding_obj.expanded)):
                    embedding_obj.expanded[quant_prop] = embedding_obj.expanded[quant_prop].astype("object")
                    # print("quant_prop", quant_prop)
                    # print("quant prop value", embedding_obj.expanded.iloc[index][quant_prop])
                    # if float(embedding_obj.expanded.iloc[index][quant_prop]) <= 0:
                    #     print("NONE")
                    quantprop_value = float(embedding_obj.expanded.iloc[index][quant_prop])
                    expanded_embedding = np.repeat(quantprop_value if quantprop_value >= 0 else 0.5, target_length)
                    # print("embedding shape", expanded_embedding.shape)
                    # print("EXPANDED EMBEDDING: ", expanded_embedding)
                    embedding_obj.expanded.at[index, quant_prop] = expanded_embedding
                    # print("embedding shape", embedding_obj.expanded.iloc[index][quant_prop].shape)

            # embedding_obj.expanded.fillna(0.5)
            # embedding_obj.expanded.replace(np.nan,0.5)
            # embedding_obj.expanded.replace({'nan': 0.5}, regex=True)
                    

            for index in range(len(embedding_obj.expanded)):
                # print("DEBUG", embedding_obj.expanded.filter(regex="quant|sem|cat").iloc[index, :].to_numpy())
                embedding_obj.expanded.at[index, "[gen] expanded_composite_embedding"] = embedding_obj.expanded.filter(regex="quant|sem|cat").iloc[index, :].to_numpy()

            # print("EXPANDED EMBEDDING: ", embedding_obj.expanded)
            # self.default_embedding_df.expanded.to_pickle("default_embedding_df_expanded.pkl")

    def reduce2twod_embedding_df(self, embedding_obj):
        if type(embedding_obj) != EmbeddingDf:
            raise TypeError("embedding_obj must be of type EmbeddingDf")
        else:
            self.expand_embedding(embedding_obj)
            embedding_obj.twod = self.info_df.copy()
            embedding_obj.twod["[gen] 2d embedding"] = None
            embedding_obj.twod["[gen] 2d embedding"] = embedding_obj.twod["[gen] 2d embedding"].astype("object")
            embedding_obj.twod["[gen] 2d embedding x"] = None
            embedding_obj.twod["[gen] 2d embedding x"] = embedding_obj.twod["[gen] 2d embedding"].astype("object")
            embedding_obj.twod["[gen] 2d embedding y"] = None
            embedding_obj.twod["[gen] 2d embedding y"] = embedding_obj.twod["[gen] 2d embedding"].astype("object")
            full_embeddings = []
            for index in range(len(embedding_obj.twod)):
                full_embedding_list = embedding_obj.expanded.iloc[index]["[gen] expanded_composite_embedding"]
                # for i in range(len(full_embedding_list)):
                #     print("index: ", index)
                #     print("DEBUG SHAPE: ", full_embedding_list[i].shape)
                full_embedding = np.concatenate(full_embedding_list).ravel().reshape(-1).flatten()
                full_embeddings.append(full_embedding)
                # print(type(ast.literal_eval(full_embedding)))
                # print("DEBUG FULL EMBEDDING: ", full_embedding)
                # print("DEBUG FULL EMBEDDING TYPE: ", type(full_embedding))
                # for i in range(len(full_embedding)):
                    # print("DEBUG FULL EMBEDDING SHAPE: ", full_embedding.shape)
                # reduced_embedding = TSNE(n_components=2, learning_rate='auto', init='random').fit_transform(full_embedding)
            reduced_embeddings = TSNE(n_components=2, learning_rate='auto', init='random').fit_transform(np.vstack(full_embeddings))
            for index in range(len(embedding_obj.twod)):
                print("DEBUG REDUCED EMBEDDING: ", reduced_embeddings[index])
                embedding_obj.twod.at[index, "[gen] 2d embedding"] = reduced_embeddings[index]
                embedding_obj.twod.at[index, "[gen] 2d embedding x"] = reduced_embeddings[index][0]
                embedding_obj.twod.at[index, "[gen] 2d embedding y"] = reduced_embeddings[index][1]
            print("embedding_obj.twod: ", embedding_obj.twod)

thisVizEmbData = VizEmbData()