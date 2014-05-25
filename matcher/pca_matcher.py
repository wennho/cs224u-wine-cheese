from baseline_matcher import LinearMatcher
import pickle
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

class PCAMatcher(LinearMatcher):

    num_dimensions = 10

    def __init__(self):
        LinearMatcher.__init__(self)

        cheese_features = pickle.load(open('../cheese_type_descriptor_mat.p', 'rb'))
        cheese_names = pickle.load(open('../cheese_names_list.p', 'rb'))

        pca = PCA(n_components=15)
        new_features = pca.fit_transform(cheese_features)

        for index, cheese_name in enumerate(cheese_names):
            self.cheeses[cheese_name] = new_features[index, :]


