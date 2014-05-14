import pickle
import numpy as np

wine_features = pickle.load(open('../wine_type_descriptor_mat.p', 'rb'))
wine_names = pickle.load(open('../wine_type_list.p', 'rb'))
cheese_features = pickle.load(open('../cheese_type_descriptor_mat.p', 'rb'))
cheese_names = pickle.load(open('../cheese_names_list.p', 'rb'))
pairings = pickle.load(open('../cheese_wine_dict.p', 'rb'))