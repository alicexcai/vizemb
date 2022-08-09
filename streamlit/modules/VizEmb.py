import pandas as pd
import numpy as np
from collections import defaultdict
from .embed import ai_embed
from sklearn.manifold import TSNE
import warnings
warnings.filterwarnings('ignore')

# generic parameter class

class Params:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# embedding dataframe class

class EmbeddingDf:
    def __init__(self):
        self.highdim = None
        self.expanded = None
        self.unraveled = None
        # self.reduced = None
        self.twod = None

# main database class

class VizEmbData:
    def __init__(self, **kwargs):
        # self.__dict__.update(kwargs) # only if necessary
        self.project_name = ""
        self.db_file = None
        self.db_filename = None
        self.unprocessed_df = None
        self.df = None
        self.colvalue_df = defaultdict()
        self.filtered_df = None
        self.info_df = None
        self.quant_df = None
        self.sem_df = None
        self.cat_df = None
        self.properties = defaultdict() # { quant: {property: {min: , max: , avg: }}, sem: {}, cat: {} }
        
        self.cat_values = defaultdict() # {cat_name1 : [cat_value1, cat_value2, ...], cat_name2 ...}
        self.parsed_cat_dfs = defaultdict() # {cat_name1 : parsed_cat1_df, cat_name2 : parsed_cat2_df, ...}
        self.cat_counts = defaultdict() # {cat_name1 : {cat_value1: #, cat_value2: #, ...}, cat_name2 ...}
        
        self.sem_embedding_length = None
        self.quant_embedding_df = None
        self.sem_embedding_df = None
        self.default_embedding_df = EmbeddingDf()
        self.specified_embedding_df = EmbeddingDf()

        self.oned_embedding_df = None

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
            self.unprocessed_df = pd.read_csv(self.db_file, encoding = "ISO-8859-1") # threw error with utf-8
        except:
            raise Exception(f"Could not load data from {self.db_file}")
    
    def process_df(self, column_dict):
        self.df = self.unprocessed_df.copy()
        self.df = self.df.filter(regex="|".join(list(column_dict.keys())))
        column_rename_dict = {col: "[" + column_dict[col] +  "] " + col for col in list(column_dict.keys())}
        self.df = self.df.rename(columns=column_rename_dict)

    def split_df(self):
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
            counted_df = self.df.filter(regex='id|title|date')
            # find unique category values
            concat_cat_values = ','.join(self.cat_df[cat_name].astype(str))
            all_cat_values = [x.strip() for x in concat_cat_values.split(',')]
            self.cat_values[cat_name] = list(set(all_cat_values))
            self.properties["cat"][cat_name] = self.cat_values[cat_name]
            # creates a column for each category value
            for cat_value in self.cat_values[cat_name]:
                for index in range(len(counted_df)):
                    # check if the category value is in the list of category values in the category column
                    counted_df.at[index, "[catval] " + cat_value] = 1 if cat_value in self.cat_df.at[index, cat_name] else 0
            # add category count dfs to dictionary, keyed by category name
            self.parsed_cat_dfs[cat_name] = counted_df

    def calculate_quantd_counts(self, quantd):
        # calculate quantitative counts by property filter
        return self.quant_df[quantd].value_counts()
        
    
    def calculate_cat_counts(self):
        # calculate categorical counts by property filter
        for cat in self.properties["cat"]:
            self.cat_counts[cat] = defaultdict()
            for cat_value in self.cat_values[cat]:
                self.cat_counts[cat][cat_value] = self.parsed_cat_dfs[cat][self.parsed_cat_dfs[cat]["[catval] " + cat_value] == 1].shape[0]
    
    def get_colvalues(self, property_filter):
        # filter df by property filter
        self.colvalue_df[property_filter] = self.df.filter(regex=property_filter)

    def filter_df(self, property_filter):
        self.filtered_df = self.df.copy()
        for prop, values in property_filter.items():
            self.filtered_df = self.filtered_df[self.filtered_df[prop].str.contains("|".join(values), na=False, regex=True)]
        return self.filtered_df

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

    def calculate_sem_embedding(self):
        # calculate semantic embedding and output embedding df
        self.sem_embedding_df = self.df.copy()
        # loop through items in dataframe and replace column text with semantic embedding
        self.sem_embedding_df["sem_embedding"] = None
        self.sem_embedding_df["sem_embedding"] = self.sem_embedding_df["sem_embedding"].astype("object")
        for index in range(len(self.sem_embedding_df)):
            for prop in list(self.properties["sem"].keys()) + list(self.properties["cat"].keys()):
                if str(self.sem_embedding_df.iloc[index][prop]) == "nan":
                    self.sem_embedding_df.at[index, prop] = np.repeat(0.5, 512)
                else:
                    self.sem_embedding_df.at[index, prop] = ai_embed([str(self.sem_embedding_df.iloc[index][prop])])
                if self.sem_embedding_length == None:
                    self.sem_embedding_length = self.sem_embedding_df.at[index, prop][0].shape[0]
            # concatenate the float values in each column into a single array
            self.sem_embedding_df.at[index, "sem_embedding"] = self.sem_embedding_df.filter(regex="sem|cat").iloc[index, :].to_numpy()

    def compose_default_embedding(self):
        # calculate composite embedding by combining quantitative and semantic embeddings
        self.calculate_quant_embedding()
        self.calculate_sem_embedding()
        self.default_embedding_df.highdim = self.df.copy()
        for index in range(len(self.df)):

            for prop in self.properties["quant"]:
                self.default_embedding_df.highdim.at[index, prop] = self.quant_embedding_df.iloc[index][prop]
            for prop in list(self.properties["sem"].keys()) + list(self.properties["cat"].keys()):
                try:
                    self.default_embedding_df.highdim.at[index, prop] = self.sem_embedding_df.iloc[index][prop][0].numpy()
                except:
                    self.default_embedding_df.highdim.at[index, prop] = self.sem_embedding_df.iloc[index][prop]
            self.default_embedding_df.highdim.at[index, "[gen] composite_embedding"] = self.default_embedding_df.highdim.filter(regex="quant|sem|cat").iloc[index, :].to_numpy()

    def expand_embedding(self, embedding_obj, weights):
        if weights == "default":
            weights = {prop : 1 for prop in list(self.properties["quant"].keys()) + list(self.properties["sem"].keys()) + list(self.properties["cat"].keys())}
        # pad embedding with constant values to make it consistent in length in all dimensions
        if type(embedding_obj) != EmbeddingDf:
            raise TypeError("embedding_obj must be of type EmbeddingDf")
        else:
            embedding_obj.expanded = self.default_embedding_df.highdim.copy()
            target_length = self.sem_embedding_length
            for quant_prop in list(self.properties["quant"].keys()):
                for index in range(len(embedding_obj.expanded)):
                    embedding_obj.expanded[quant_prop] = embedding_obj.expanded[quant_prop].astype("object")
                    quantprop_value = float(embedding_obj.expanded.iloc[index][quant_prop])
                    expanded_embedding = np.repeat(quantprop_value if quantprop_value >= 0 else 0.5, target_length*weights[quant_prop])
                    embedding_obj.expanded.at[index, quant_prop] = expanded_embedding
            for text_prop in list(self.properties["sem"].keys()) + list(self.properties["cat"].keys()):
                for index in range(len(embedding_obj.expanded)):
                    embedding_obj.expanded[quant_prop] = embedding_obj.expanded[text_prop].astype("object")
                    textprop_value = embedding_obj.expanded.iloc[index][text_prop]
                    expanded_embedding = np.repeat(textprop_value, weights[text_prop])
                    embedding_obj.expanded.at[index, text_prop] = expanded_embedding
        
            for index in range(len(embedding_obj.expanded)):
                embedding_obj.expanded.at[index, "[gen] expanded_composite_embedding"] = embedding_obj.expanded.filter(regex="quant|sem|cat").iloc[index, :].to_numpy()

    def reduce2twod_embedding_df(self, embedding_obj, weights = "default"):
        if type(embedding_obj) != EmbeddingDf:
            raise TypeError("embedding_obj must be of type EmbeddingDf")
        else:
            self.expand_embedding(embedding_obj, weights = weights)
            embedding_obj.twod = self.df.copy()
            embedding_obj.twod["[gen] 2d embedding"] = None
            embedding_obj.twod["[gen] 2d embedding"] = embedding_obj.twod["[gen] 2d embedding"].astype("object")
            embedding_obj.twod["[gen] 2d embedding x"] = None
            embedding_obj.twod["[gen] 2d embedding x"] = embedding_obj.twod["[gen] 2d embedding"].astype("object")
            embedding_obj.twod["[gen] 2d embedding y"] = None
            embedding_obj.twod["[gen] 2d embedding y"] = embedding_obj.twod["[gen] 2d embedding"].astype("object")
            full_embeddings = []
            for index in range(len(embedding_obj.twod)):
                full_embedding_list = embedding_obj.expanded.iloc[index]["[gen] expanded_composite_embedding"]
                full_embedding = np.concatenate(full_embedding_list).ravel().reshape(-1).flatten()
                if index == 0: last_shape = full_embedding.shape
                if full_embedding.shape == last_shape:
                    full_embeddings.append(full_embedding)
                    last_shape = full_embedding.shape
            embedding_obj.unraveled = np.array(full_embeddings)
            reduced_embeddings = TSNE(n_components=2, learning_rate='auto', init='random').fit_transform(np.vstack(full_embeddings))
            for index in range(len(embedding_obj.twod)):
                try:
                    embedding_obj.twod.at[index, "[gen] 2d embedding"] = reduced_embeddings[index]
                    embedding_obj.twod.at[index, "[gen] 2d embedding x"] = reduced_embeddings[index][0]
                    embedding_obj.twod.at[index, "[gen] 2d embedding y"] = reduced_embeddings[index][1]
                except:
                    embedding_obj.twod.drop(index, inplace=True)

    def reduce2oned_embedding_df(self):
        self.oned_embedding_df = self.default_embedding_df.highdim.copy()
        for prop in list(self.properties["sem"].keys()) + list(self.properties["cat"].keys()):
            full_embeddings = self.oned_embedding_df[prop].to_numpy()
            reduced_embeddings = TSNE(n_components=1, learning_rate='auto', init='random').fit_transform(np.vstack(full_embeddings))
            for index in range(len(self.oned_embedding_df)):
                self.oned_embedding_df.at[index, prop] = reduced_embeddings[index][0]

thisVizEmbData = VizEmbData()